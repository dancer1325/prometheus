## Overview

* ==
  * `mantine-ui`
    * Prometheus' NEW React-based web UI 
      * 👀by default, served by Prometheus👀
    * | npm workspace == `modules` | npm workspace
    * hot-reload
      * == if you edit the source code -> reload the app
  * `react-app`
    * Prometheus' ⚠️OLD (2.x)⚠️ React-based web UI
      * if you want to use it -> `--enable-feature=old-ui`
    * hot-reload
  * `modules`
    * == shared npm modules
      * allows
        * editing PromQL code 
          * -- via -- [CodeMirror](https://codemirror.net/)
    * uses
      * React apps
      * external consumers
        * _Examples:_ [Thanos](https://thanos.io/)
    * ❌NOT hot reload ❌ -> make 
      * | this path,
        ```
        npm run build:module
        ```
  * `static`
    * == BOTH (NEW & OLD) React apps' build output directory 
    * compiled | Prometheus binary
      * you can disable it
  * helper files / 
    * build BOTH React application's UI assets
    * compile BOTH React application's UI assets | Prometheus binary

### Pre-requisites

* npm >= v10
* node >= v22

### Installing npm dependencies

* | root path
    ```bash
    make ui-build
    ```
  * == | this path,
    ```
    bash build_ui.sh --all
    ```

* recommendations
  * | [mantine-ui/](mantine-ui) OR ANY [module/](module)'s sub folder,
    * ❌NOT run `npm install`❌
      * Reason: 🧠MUST be installed ONLY -- via -- "web/ui"'s npm workspace setup 

### how to run local development server?

* if you want to run 
  * NEW React app,
    * | this path,
      ```
      npm run start
      ```
    * | browser, 
      * http://localhost:5173/
  * OLD UI,
    * | "[react-app/](react-app)",
      ```
      npm run start
      ```
    * | browser,
      * http://localhost:5173/

### Proxying API requests -- to a -- Prometheus backend server

* web UI
  * can
    * fetch data -- from -- Prometheus server  
    * display data -- from -- Prometheus server
  * requires
    * | [mantine-ui/vite.config.ts](mantine-ui/vite.config.ts),
      * ⚠️proxy configuration ⚠️ 

    [browser] ----> [localhost:5173 (dev server)] --(proxy API requests)--> [localhost:9090 (Prometheus)]

* proxy configuration
  * if you want to connect to HTTPS-based server -> set `changeOrigin: true`
    * _Example:_ Prometheus server | https://prometheus.demo.prometheus.io/

    ```typescript, title=vite.config.ts
    import { defineConfig } from "vite";
    import react from "@vitejs/plugin-react";
    
    // https://vitejs.dev/config/
    export default defineConfig({
      base: '',
      plugins: [react()],
      server: {
        proxy: {
          "/api": {
            target: "https://prometheus.demo.prometheus.io/",
            changeOrigin: true,
          },
          "/-/": {
            target: "https://prometheus.demo.prometheus.io/",
            changeOrigin: true,
          },
        },
      },
    });
    ```

### how to run tests?

* if you want to run tests -- for -- 
  * NEW React app & ALL modules
    * | this path,
      ```bash
      npm run test
      ```
  * OLD UI, 
    * | "[react-app/](react-app)"
      ```bash
      npm run test
      ```
  * specific module,
    * | "[module/](module)"
      ```bash
      npm run test
      ```

* ways to run tests
  * interactive watch mode
    ```bash
    npm run test
    ```
  * ONLY 1! & then exit
    ```bash
    CI=true npm test
    ```

### Building the app for production

To build a production-optimized version of both React app versions to the `static/{react-app,mantine-ui}` output directories, run:

    npm run build

**NOTE:** You will likely not need to do this directly
* Instead, this is taken care of by the `build` target in the main Prometheus `Makefile` when building the full binary.

### Upgrading npm dependencies

As this is a monorepo containing multiple npm packages, you will have to upgrade dependencies in every package individually (in all sub folders of `module`, `react-app`, and `mantine-ui`).

Then, run `npm install` in `web/ui` and `web/ui/react-app` directories, but not in the other sub folders / sub packages (this won't produce the desired results due to the npm workspace setup).

### Integration into Prometheus

To build a Prometheus binary that includes a compiled-in version of the production build of both React app versions, change to the
root of the repository and run:

```bash
make build
```

This installs dependencies via npm, builds a production build of both React apps, and then finally compiles in all web assets into the Prometheus binary.

### Serving UI assets from the filesystem

By default, the built web assets are compressed (via the main Makefile) and statically compiled into the Prometheus binary using Go's `embed` package.

During development it can be convenient to tell the Prometheus server to always serve its web assets from the local filesystem (in the `web/ui/static` build output directory) without having to recompile the Go binary
* To make this work, remove the `builtinassets` build tag in the `flags` entry in `.promu.yml`, and then run `make build` (or build Prometheus using `go build ./cmd/prometheus`).

Note that in most cases, it is even more convenient to just use the development web server via `npm start` as mentioned above, since serving web assets like this from the filesystem still requires rebuilding those assets via `make ui-build` (or `npm run build`) before they can be served.

### Using prebuilt UI assets

If you are only working on the Prometheus Go backend and don't want to bother with the dependencies or the time required for producing UI builds, you can use the prebuilt web UI assets available with each Prometheus release (`prometheus-web-ui-<version>.tar.gz`)
* This allows you to skip building the UI from source.

1. Download and extract the prebuilt UI tarball:
   ```bash
   tar -xvf prometheus-web-ui-<version>.tar.gz -C web/ui
   ```

2. Build Prometheus using the prebuilt assets by passing the following parameter
   to `make`:
   ```bash
   make PREBUILT_ASSETS_STATIC_DIR=web/ui/static build
   ```

This will include the prebuilt UI files directly in the Prometheus binary, avoiding the need to install npm or rebuild the frontend from source.
