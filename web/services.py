import csv
from os import write

from web.models import Articles


def export_articles_csv(articles, response):
    writer = csv.writer(response)
    writer.writerow(
        ("Title", "Content", "Create date")
    )
    for article in articles:
        writer.writerow(
            (article.title, article.content, article.create_date)
        )

    return response


def import_csv(file, user):
    str_from_file = (row.decode() for row in file)
    reader = csv.DictReader(str_from_file)
    new_articles = []
    for row in reader:
        new_articles.append(
            Articles(
                title=row["Title"],
                content=row["Content"],
                create_date=row["Create date"],
                user=user
            )
        )
    Articles.objects.bulk_create(new_articles)