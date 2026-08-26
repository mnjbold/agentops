"""Build base64 Coolify custom_labels for the agentops app with the agentops.getbijou.xyz domain."""
import base64
import sys

app_uuid = sys.argv[1] if len(sys.argv) > 1 else "<APP_UUID>"
domain = "https://agentops.getbijou.xyz"
port = "80"

labels = f"""traefik.enable=true
traefik.http.middlewares.gzip.compress=true
traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https
traefik.http.routers.http-0-{app_uuid}.entryPoints=http
traefik.http.routers.http-0-{app_uuid}.middlewares=redirect-to-https
traefik.http.routers.http-0-{app_uuid}.rule=Host(`{domain.replace("https://","")}`) && PathPrefix(`/`)
traefik.http.routers.http-0-{app_uuid}.service=http-0-{app_uuid}
traefik.http.routers.https-0-{app_uuid}.entryPoints=https
traefik.http.routers.https-0-{app_uuid}.middlewares=gzip
traefik.http.routers.https-0-{app_uuid}.rule=Host(`{domain.replace("https://","")}`) && PathPrefix(`/`)
traefik.http.routers.https-0-{app_uuid}.service=https-0-{app_uuid}
traefik.http.routers.https-0-{app_uuid}.tls.certresolver=letsencrypt
traefik.http.routers.https-0-{app_uuid}.tls=true
traefik.http.services.http-0-{app_uuid}.loadbalancer.server.port={port}
traefik.http.services.https-0-{app_uuid}.loadbalancer.server.port={port}
caddy_0={domain}
caddy_0.encode=zstd gzip
caddy_0.handle_path.0_reverse_proxy={{{{upstreams {port}}}}}
caddy_0.handle_path=/*
caddy_0.header=-Server
caddy_0.try_files={{{{path}}}} /index.html /index.php
caddy_ingress_network=coolify
"""

b64 = base64.b64encode(labels.encode("utf-8")).decode("ascii")
print(b64)
