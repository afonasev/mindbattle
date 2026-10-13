```json
{
  "status": "binding-corrections",
  "sourceBinding": {
    "sourceId": "METEINFO_PRECIP",
    "path": "docs/content-audits/question-quality-wave-7/weather-climate/first10-native-01a12b0a-acb9-78b1-9b8b-823fc535ddd9/sources/meteoinfo-precip-terms.html",
    "bytes": 65113,
    "correctBodySha256": "2011bcaeffd8e3dc8270da507479a8bdc37d7f37b67b95bd6b570ca6c12f52da",
    "replacesErroneousSha256": "2011bcaeffd8e3dc8270da507479a8bdc37d7f37b67b95bd6b5706a1c12f52da"
  },
  "cardBinding": {
    "cardId": "weather-climate-hail-ice-balls",
    "field": "answers[0].note",
    "literal": "NWS определяет град как ледяные шарики или комки диаметром более 5 мм.",
    "hashRecipe": "SHA-256 UTF-8 json.dumps(stringValue, sort_keys=True, ensure_ascii=False, separators=(',', ':')); no trailing newline.",
    "correctSha256": "73e45a126c00bab6c6b133154b4dc3c01882ff841669b7dd948c40ae29284c10",
    "replacesErroneousSha256": "73e45e126c00bab6c6b133154b4dc3c01882ff841669b7dd948c40ae29284c10"
  },
  "qualityCredit": 0
}
```