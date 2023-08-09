# am-train-location-display
Train vehicle location for real life display


## Notes for future Josh

* If you get the error `Module google.transit not found` have to make sure the `google/transit` folders/files are in the correct place in either/both of `site-packages` and `dist packages` and that `protobuf` is installed
* Steps to get it to work (fingers crossed):
  * `python -m pip install --upgrade gtfs-realtime-bindings`
  * `python -m pip install --upgrade protobuf`
* There's some werid  stuff, as usual, going on with the dependencies and packages etc
* You may still need to manually git clone from `https://github.com/MobilityData/gtfs-realtime-bindings.git` and copy into the correct `site-packages` area.