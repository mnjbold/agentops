FROM nginx:alpine
LABEL org.opencontainers.image.source="https://github.com/mybijouai-creator/agentops"
LABEL org.opencontainers.image.description="W3J AgentOps dashboard (single-page HTML)"
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
CMD ["nginx", "-g", "daemon off;"]
