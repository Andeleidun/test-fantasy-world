# CI regeneration gate

The pull-request workflow regenerates Strategy A geometry with the pinned Cartopy stack, runs the dated constraint and physical-test validators, runs the existing geological audit, replays the cached paleolatitude analysis, and uploads the resulting `docs/global-geography-trial` directory as a workflow artifact.

Generated geometry and metrics committed before that run are not accepted as current evidence unless they match the regenerated outputs. This file exists to make the regeneration requirement explicit during the reconstruction branch review.
