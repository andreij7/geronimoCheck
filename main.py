from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import requests
import json

id = "f60d7aa9-c066-4487-8f37-2606a3b0305c"
geronimoUrl = 'http://geronimo-diagnostic-api-east.staging.gannettdigital.com/api/v1/aggregates/%s?transform=authoring-export' % id

r = requests.get(url=geronimoUrl)
geronimoResult = r.json()

with open('geronimo.txt', 'w') as outfile:
    json.dump(geronimoResult, outfile)

client = Client(
    retries=3,
    transport=RequestsHTTPTransport(
        url='https://origin-staging-content-api.gannettdigital.com/authoring',
        headers={'x-sitecode': 'USAT', 'x-api-key': ''},
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

with open('capi.txt', 'w') as outfile:
    json.dump(asset, outfile)

from deepdiff import DeepDiff

ddiff = DeepDiff(geronimoResult, asset, ignore_order=True)
print(ddiff)