let
  _pkgs = import <nixpkgs> {};
in
{ pkgs ? import (_pkgs.fetchFromGitHub { owner = "NixOS";
                                         repo = "nixpkgs-channels";
                                         # nixos-unstable @2019-02-04
                                         rev = "2d6f84c1090ae39c58dcec8f35a3ca62a43ad38c";
                                         sha256 = "0l8b51lwxlqc3h6gy59mbz8bsvgc0q6b3gf7p3ib1icvpmwqm773";
                                       }) {}
}:

with pkgs;

mkShell {
  buildInputs = [
    bash
    python3
    python3Packages.black
    python3Packages.netaddr
    python3Packages.packet-python
  ];
}
