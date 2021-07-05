import logging

from django.core.management.base import BaseCommand
from cms.publications.models import PublicationPublicationTypeRelationship
from cms.categories.models import PublicationType

logger = logging.getLogger(__name__)

changes = {
    60: 59,
    61: 59,  # Case Study
    64: 63,  # Data and statistics
    66: 65,  # Decision
    70: 69,
    71: 69,  # Form
    73: 72,
    74: 72,
    75: 72,  # Guidance
    80: 79,  # Letter
    82: 81,  # Meeting papers and minutes
    85: 86,  # Newsletter -> Newsletter or bulletin
    87: 88,
    89: 88,  # Policy, Policy or strategy -> Policy and strategy
    92: 91,  # Promotional material
    95: 94,
    96: 94,
    97: 94,
    98: 94,  # Report
    100: 99,  # Research
    102: 101,  # Service Specification
    104: 103,  # Standard operating procedure
    108: 107,  # Template
}


def delete_redundant_publicationtypes():
    """Remove the publication types that should be empty, now.
    (These are the records that give the types names and sources (if they haven't been removed)
    """
    pubtypes = PublicationType.objects.all()
    length = len(pubtypes)
    count = 0
    for pubtype in pubtypes:
        if pubtype.id in changes.keys():
            count = count + 1
            pubtype.delete()
    print(f"✅ {count} / {length} PublicationTypes deleted.")


def deduplicate_publicationtypes():
    """Replace the publication type IDs associated with each publication with the ID
    of the publication type we're keeping."""
    relationships = PublicationPublicationTypeRelationship.objects.all()
    count = 0
    for relation in relationships:
        type_id = relation.publication_type_id
        if type_id in changes.keys():
            count = count + 1
            relation.publication_type_id = changes[type_id]
            relation.save()
            relation.validate_unique()

    print(
        f"✅ {count} / {len(relationships)} Publication/PublicationType relationships changed."
    )

    ##################################
    return


class Command(BaseCommand):
    """
    Each sub_site had a different set of 'publication types', but we want to unify these.
    help = "Deduplicate publication types"
    """

    def handle(self, *args, **options):

        deduplicate_publicationtypes()
        delete_redundant_publicationtypes()