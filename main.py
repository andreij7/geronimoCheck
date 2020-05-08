from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import requests
import json
import sys
import os

ids_file = sys.argv[1]

with open(ids_file) as f:
  data = json.load(f)

for id in data['ids']:
  geronimoUrl = 'http://geronimo-diagnostic-api-east.staging.gannettdigital.com/api/v1/aggregates/%s?transform=authoring-export' % id

  r = requests.get(url=geronimoUrl)
  geronimoResult = r.json()

  with open(f'geronimo_{id}.txt', 'w') as outfile:
      json.dump(geronimoResult, outfile)

  client = Client(
      retries=3,
      transport=RequestsHTTPTransport(
          url='https://origin-staging-content-api.gannettdigital.com/authoring',
          headers={'x-sitecode': 'USAT', 'x-api-key': os.environ['CONTENT_API_KEY']},
      )
  )

  # Variables
  request = '''
    query authoringAsset {
    asset(id: "%s") {
      aggregateName
      assetGroup {
        name
        id
        property {
          id
          name
        }
        site {
          code
          id
          name
        }
      }
      authoringTypeCode
      body
      createdByUser
      contentSourceCode
      classificationId
      headline
      pageTitle
      urlEnding
      brief
      contentTags {
        id
        isAutoTag
        isDisabled
        name
      }
      systemTags {
        id
        isAutoTag
        isDisabled
      }
      contributors: contributorIds
      byline
      contentSourceName
      highlights
      notes
      slug
      frontAssignments
      advertisingTagIds
      contentQueueDate
      copiedTo
      paywallType
      evergreen
      createdDate
      printFolderName
      printRank
      desktopOnly
      evergreen
      sendToNewsPlayer
      readerCommentsEnabled
      planningStatus
      createdBySystem
      currentVersionDate
      currentVersionHash
      doNotShare
      eventState {
        headHash
        requestedHash
      }
      friendlyId
      id
      initialPublishedDate
      isPublishable
      noAdvertising
      pageUrl
      primaryContentTagId
      promoHeadline
      promoImageId
      sentToNewsgate
      sharedWithNetwork
      status
      updatedBySystem
      updatedByUser
      updatedDate
      userUpdatedDate
      standout
      isCurrentlyPublished
      promoImageId
      associatedAssets {
        id
      }
      brief
    }
  }
  '''
  query = gql(request % id)
  contentApiResult = client.execute(query)
  asset = contentApiResult['asset']

  with open(f'capi_{id}.txt', 'w') as outfile:
      json.dump(asset, outfile)

  from deepdiff import DeepDiff

  ddiff = DeepDiff(geronimoResult, asset, ignore_order=True)
  print(ddiff)