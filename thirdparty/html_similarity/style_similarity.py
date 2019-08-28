from thirdparty.parsel import Selector


def get_classes(html):
    doc = Selector(text=html)
    classes = set(doc.xpath('//*[@class]/@class').extract())
    result = set()
    for cls in classes:
        for _cls in cls.split():
            result.add(_cls)
    return result


def jaccard_similarity(set1, set2):
    set1 = set(set1)
    set2 = set(set2)
    intersection = len(set1 & set2)

    if len(set1) == 0 and len(set2) == 0:
        return 1.0

    denominator = len(set1) + len(set2) - intersection
    return intersection / max(denominator, 0.000001)


def style_similarity(page1, page2):
    """
    Computes CSS style Similarity between two DOM trees

    A = classes(Document_1)
    B = classes(Document_2)

    style_similarity = |A & B| / (|A| + |B| - |A & B|)

    :param page1: html of the page1
    :param page2: html of the page2
    :return: Number between 0 and 1. If the number is next to 1 the page are really similar.
    """
    classes_page1 = get_classes(page1)
    classes_page2 = get_classes(page2)
    return jaccard_similarity(classes_page1, classes_page2)
