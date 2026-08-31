# RC104 Harbor shipment readout

Artifact `rc104-harbor-ferry-c` was sampled against `release/rc-104`.

Shipment count smoke: 4,019 route rows, matching the dashboard export.

Line sample: `harbor/ferry/ship-614` still appears as `status=active` and `include_in_export=true` although the partner payload carries `voidReason: "carrier-reversal"`.

Interpretation: dashboard count parity is not sufficient for release acceptance.
