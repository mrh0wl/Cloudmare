"""Interact with the Censys Seeds API."""
from typing import Optional

from .api import CensysAsmAPI

SEED_TYPES = ["IP_ADDRESS", "DOMAIN_NAME", "CIDR", "ASN"]


class Seeds(CensysAsmAPI):
    """Seeds API class."""

    base_path = "seeds"

    def get_seeds(
        self, seed_type: Optional[str] = None, label: Optional[str] = None
    ) -> dict:
        """Requests seed data.

        Args:
            seed_type (str):
                Optional; Seed type ['IP_ADDRESS', 'DOMAIN_NAME', 'CIDR', 'ASN'].
            label (str): Optional; Seed label.

        Returns:
            dict: Seed search results.
        """
        args = {}
        if seed_type:
            args["type"] = seed_type
        if label:
            args["label"] = label
        return self._get(self.base_path, args=args)["seeds"]

    def get_seed_by_id(self, seed_id: int) -> dict:
        """Requests seed data by ID.

        Args:
            seed_id (int): Seed ID to get.

        Returns:
            dict: Seed search result.
        """
        path = f"{self.base_path}/{seed_id}"

        return self._get(path)

    def add_seeds(self, seeds: list, force: Optional[bool] = None) -> dict:
        """Add seeds to the ASM platform.

        Args:
            seeds (list): List of seed objects to add.
            force (bool, optional): Forces replace operation.

        Returns:
            dict: Added seeds results.
        """
        data = {"seeds": seeds}
        args = {"force": force}

        return self._post(self.base_path, args=args, data=data)

    def replace_seeds_by_label(
        self, label: str, seeds: list, force: Optional[bool] = None
    ) -> dict:
        """Replace seeds in the ASM platform by label.

        Args:
            label (str): Label name to replace by.
            seeds (list): List of seed objects to add.
            force (bool): Optional; Forces replace operation.

        Returns:
            dict: Added and removed seeds results.
        """
        data = {"seeds": seeds}
        args = {"label": label, "force": force}

        return self._put(self.base_path, args=args, data=data)

    def delete_seeds_by_label(self, label: str) -> dict:
        """Delete seeds in the ASM platform by label.

        Args:
            label (str): Label name to delete by.

        Returns:
            dict: Delete results.
        """
        args = {"label": label}

        return self._delete(self.base_path, args=args)

    def delete_seed_by_id(self, seed_id: int) -> dict:
        """Delete a seed in the ASM platform by id.

        Args:
            seed_id (int): Seed ID to delete by.

        Returns:
            dict: Delete results.
        """
        path = f"{self.base_path}/{seed_id}"

        return self._delete(path)
