import thirdparty.requests as requests
import json


class SecurityTrailsError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)


class SecurityTrailsForbidden(SecurityTrailsError):
    def __init__(self):
        self.message = "Access Forbidden: you need a more expensive plan"
        SecurityTrailsError.__init__(self, self.message)


class SecurityTrailsTooManyRequests(SecurityTrailsError):
    def __init__(self):
        self.message = "Too Many Requests: You are out of credits"
        SecurityTrailsError.__init__(self, self.message)


class SecurityTrailsInvalidKey(SecurityTrailsError):
    def __init__(self):
        self.message = "Unauthorized: You did not provide a valid API key"
        SecurityTrailsError.__init__(self, self.message)


class SecurityTrailsInvalidQuery(SecurityTrailsError):
    def __init__(self, msg):
        self.message = "Invalid query: {}".format(msg)
        SecurityTrailsError.__init__(self, self.message)


class SecurityTrails(object):
    def __init__(self, key):
        self.api_key = key
        self.base_url = "https://api.securitytrails.com/v1/"
        self.SEARCH_FILTERS = ['ipv4', 'ipv6', 'apex_domain', 'keyword', 'mx',
                'ns', 'cname', 'subdomain', 'soa_email', 'tld', 'whois_email',
                'whois_street1', 'whois_street2', 'whois_street3',
                'whois_street4', 'whois_telephone', 'whois_postalCode',
                'whois_organization', 'whois_name', 'whois_fax',  'whois_city']

    def _get(self, path, params={}):
        headers = {'APIKEY': self.api_key}
        r = requests.get(self.base_url + path, params=params, headers=headers)
        if r.status_code != 200:
            if r.status_code == 403:
                raise SecurityTrailsForbidden()
            elif r.status_code == 429:
                raise SecurityTrailsTooManyRequests()
            else:
                raise SecurityTrailsError('Bad HTTP Status Code %i' % r.status_code)
        return r.json()

    def _post(self, path, params={}, data={}):
        headers = {'APIKEY': self.api_key}
        r = requests.post(
            self.base_url + path,
            params=params,
            headers=headers,
            data=data
        )
        if r.status_code != 200:
            if r.status_code == 403:
                raise SecurityTrailsForbidden()
            elif r.status_code == 429:
                raise SecurityTrailsTooManyRequests()
            elif r.status_code == 401:
                raise SecurityTrailsInvalidKey()
            elif r.status_code == 400:
                raise SecurityTrailsInvalidQuery(r.json()['message'])
            else:
                raise SecurityTrailsError('Bad HTTP Status Code %i' % r.status_code)
        return r.json()

    # ------------------------------- General ---------------------------------
    def ping(self):
        """
        You can use this simple endpoint to test your authentication and access
        to the SecurityTrails API.
        https://docs.securitytrails.com/v1.0/reference#ping

        Args:
            None

        Returns:
            A dict created from the JSON returned by Security Trails
            Example: {'success': True}

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('ping')

    def usage(self):
        return self._get('account/usage')

    def scroll(self, scroll_id):
        """
        A fast and easy way to fetch many results. Currently only available for
        the DSL API endpoints.
        https://docs.securitytrails.com/v1.0/reference#scroll

        Args:
            scroll_id: The scroll_id returned in the scroll request (int)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('scroll/%i' % scroll_id)

    # ---------------------------- Domain Details -----------------------------
    def domain_info(self, domain):
        """
        Returns the current data about the given domain. In addition to
        the current data, you also get the current statistics associated
        with a particular record. For example, for a records you'll get
        how many other domains have the same IP.
        https://docs.securitytrails.com/v1.0/reference#get-domain

        Args:
            hostname: domain (String)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('domain/%s' % domain)

    def domain_subdomains(self, hostname):
        """
        Returns subdomains for a given hostname
        https://docs.securitytrails.com/v1.0/reference#list-subdomains

        Args:
            hostname: Domain (String)

        Returns:
            A dict created from the JSON returned by Security Trails
            Example: {'subdomains': ['staging', 'www'],
            'endpoint': '/v1/domain/HOSTNAME/subdomains'}

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('domain/%s/subdomains' % hostname)

    def domain_tags(self, hostname):
        """
        Returns tags for a given hostname
        https://docs.securitytrails.com/v1.0/reference#list-tags

        Args:
            hostname: Domain (String)

        Returns:
            A dict created from the JSON returned by Security Trails
            Example: {'tags': [], 'endpoint': '/v1/domain/HOSTNAME/tags'}

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('domain/%s/tags' % hostname)

    def domain_associated(self, hostname, page=1):
        """
        Find all domains that are related to a domain you input
        https://docs.securitytrails.com/v1.0/reference#find-associated-domains

        Args:
            hostname: Domain (String)
            page: The page of the returned results.

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get(
            'domain/%s/associated' % hostname,
            params={'page': page}
        )

    def domain_whois(self, hostname):
        """
        Returns the current WHOIS data about a given domain with the stats
        merged together
        https://docs.securitytrails.com/v1.0/reference#get-whois

        Args:
            hostname: domain (String)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('domain/{}/whois'.format(hostname))

    # ------------------------ Domain Search ----------------------------------
    def domain_search(self, filter, include_ips=True, page=1):
        """
        Filter and search specific records using this endpoint.
        https://docs.securitytrails.com/v1.0/reference

        Args:
            filter: filter for the research as {"ipv4": "IP"}
            include_ips: Resolves any A records and additionally returns IP
            addresses. (default is true)
            page: The page of the returned results. (default is 1)


        """
        if not isinstance(filter, dict):
            raise SecurityTrailsError("Filter should be a dict")

        invalid_filters = [k for k in filter.keys() if k not in self.SEARCH_FILTERS]
        if len(invalid_filters) > 0:
            raise SecurityTrailsError("Unknown filters : {}".format(",".join(invalid_filters)))
        f = {'filter': filter}
        return self._post(
            'domains/list',
            params={
                'include_ips': str(include_ips).lower(),
                'page': page
            },
            data=json.dumps(f)
        )

    def domain_search_dsl(self, query, include_ips=True, page=1, scroll=False):
        """
        Filter and search specific records using our DSL with this endpoint
        https://docs.securitytrails.com/v1.0/reference#search-domain-dsl

        Args:
            query: DSL query
            include_ips: Resolves any A records and additionally returns IP
            addresses. (default is true)
            page: The page of the returned results. (default is 1)
            scroll: request scrolling (default is False)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._post(
            'domains/list',
            params={
                'include_ips': str(include_ips).lower(),
                'page': page,
                'scroll': scroll
            },
            data=json.dumps({'query': query})
        )

    def domain_search_stats(self, filter):
        """
        https://docs.securitytrails.com/v1.0/reference#search-count

        Args:
            filter: filter for the research

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        f = {'filter': filter}
        return self._post(
            'domains/stats',
            data=json.dumps(f)
        )

    # ------------------------------- History ---------------------------------
    def domain_history_dns(self, hostname, type='a', page=1):
        """
        Lists out specific historical information about the given hostname
        parameter
        https://docs.securitytrails.com/v1.0/reference#dns-history-by-record-type

        Args:
            hostname: domain (string)
            type: allowed values: a, aaaa, mx, ns, soa or txt
            page: 1

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        if type not in ['a', 'aaaa', 'soa', 'mx', 'ns', 'txt']:
            raise SecurityTrailsError('Invalid DNS type given')
        return self._get(
            'history/%s/dns/%s' % (hostname, type),
            params={'page': page}
        )

    def domain_history_whois(self, hostname, page=1):
        """
        Returns historical WHOIS information about the given domain
        https://docs.securitytrails.com/v1.0/reference#whois-history-by-domain

        Args:
            hostname: domain (String)
            page: page (int, default is 1)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get(
            'history/%s/whois' % hostname,
            params={'page': page}
        )

    # ------------------------------------ IPs --------------------------------
    def ips_nearby(self, ipaddress):
        """
        Returns the neighbors in any given IP level range and essentially
        allows you to explore closeby IP addresses.
        https://docs.securitytrails.com/v1.0/reference#ips

        Args:
            ipaddress: IP Address (string)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._get('ips/nearby/%s' % ipaddress)

    def ips_search_dsl(self, query, page=1):
        """
        Search for an IP address using DSL
        https://docs.securitytrails.com/v1.0/reference#search-ips-dsl

        Args:
            query: DSL query (string)
            page: integer, default is 1

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._post(
            'ips/list',
            params={'page': page},
            data=json.dumps({'query': query})
        )

    def ips_search_stats(self, query):
        """
        Stats on a DSL IP query
        https://docs.securitytrails.com/v1.0/reference#ip-search-statistics

        Args:
            query: DSL query (string)

        Returns:
            A dict created from the JSON returned by Security Trails

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        return self._post(
            'ips/stats',
            data=json.dumps({'query': query})
        )

    # ------------------------------- Feeds -----------------------------------
    def feeds_domains(self, type, filter=None, tld=None, ns=True):
        """
        Fetch zone files including authoritative nameservers with ease
        https://docs.securitytrails.com/v1.0/reference#feeds

        Args:
            type: valid values are "all", "dropped" or "new"
            filter: valid values are "cctld" and "gtld"
            tld: Can be used to only return domains of a specific tld
                such as "com"
            ns: show nameservers in the list

        Returns:
            The output is a .csv.gz binary file.

        Raises:
            SecurityTrailsError: if anything else than 200 OK is returned
        """
        params = {'ns': ns}
        if type not in ['all', 'dropped', 'new', 'registered']:
            raise SecurityTrailsError('Invalid type')
        if filter:
            if filter not in ['cctld', 'gtld']:
                raise SecurityTrailsError('Invalid type')
            else:
                params['filter'] = filter
        if tld:
            params['tld'] = tld
        headers = {'APIKEY': self.api_key}
        r = requests.get(
            self.base_url + 'feeds/domains/%s' % type,
            params=params,
            headers=headers
        )
        if r.status_code != 200:
            if r.status_code == 403:
                raise SecurityTrailsForbidden()
            elif r.status_code == 429:
                raise SecurityTrailsTooManyRequests()
            else:
                raise SecurityTrailsError('Bad HTTP Status Code %i' % r.status_code)
        return r.content
