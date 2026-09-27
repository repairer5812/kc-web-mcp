# Third-party components

This repository provides deployment configuration and verification scripts. It
installs the following upstream components without claiming authorship of them.
The repository's MIT license does not replace their licenses.

## SpaceDock 0.1.6 — MIT

Source: https://github.com/starlove7/spacedock

Docker builds pinned commit `41df6ed1519242e742079c84989cd15b5a4e441b`.
Portlane changes the approval presentation and adds static presentation routes;
upstream OAuth request validation and token logic remain in place. The customized
binary identifies its version as `0.1.6-portlane.1`.

## Pretendard 1.3.9 — SIL Open Font License 1.1

Source: https://github.com/orioncactus/pretendard/tree/v1.3.9
The unmodified variable font is self-hosted. Full copyright and license notice:
`licenses/Pretendard-OFL.txt`.

## SpaceDock license text

MIT License

Copyright (c) 2026 starlove7

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## cloudflared 2026.9.3 — Apache-2.0

Source and license: https://github.com/cloudflare/cloudflared/blob/2026.9.3/LICENSE

The Docker build copies the executable from Cloudflare's official image.
Retain the upstream Apache-2.0 license and applicable notices when redistributing
the built image. See `licenses/cloudflared-LICENSE`.

## Node.js and Debian packages

The runtime derives from the official Node.js Debian image. Node.js license:
https://github.com/nodejs/node/blob/main/LICENSE. Debian packages carry their
own licenses under `/usr/share/doc/*/copyright` in the built image.

## Design reference

DevSpace (https://github.com/Waishnav/devspace) was reviewed as a reference.
No DevSpace implementation code is included in this repository.
