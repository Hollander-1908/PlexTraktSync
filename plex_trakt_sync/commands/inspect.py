import click

from plex_trakt_sync.factory import factory
from plex_trakt_sync.version import git_version_info


@click.command()
@click.argument('input')
def inspect(input):
    """
    Inspect details of an object
    """

    git_version = git_version_info() or 'Unknown version'
    print(f"PlexTraktSync inspect [{git_version}]")

    plex = factory.plex_api()
    mf = factory.media_factory()

    if input.isnumeric():
        input = int(input)

    pm = plex.fetch_item(input)
    print(f"Inspecting {input}: {pm}")

    url = plex.media_url(pm)
    print(f"URL: {url}")

    media = pm.item
    print(f"Media.Guid: '{media.guid}'")
    if not pm.is_legacy_agent:
        print(f"Media.Guids: {media.guids}")

    if media.type in ["episode", "movie"]:
        audio = media.media[0].parts[0].audioStreams()[0]
        print(f"Audio: '{audio.audioChannelLayout}', '{audio.displayTitle}'")

        video = media.media[0].parts[0].videoStreams()[0]
        print(f"Video: '{video.codec}'")

    print("Guids:")
    for guid in pm.guids:
        print(f"  Guid: {guid}, Id: {guid.id}, Provider: {guid.provider}")

    print(f"Metadata: {pm.to_json()}")

    m = mf.resolve_any(pm)
    if not m:
        return

    print(f"Trakt: {m.trakt_url}")
    print(f"Watched on Plex: {m.watched_on_plex}")
    print(f"Warched on Trakt: {m.watched_on_trakt}")
