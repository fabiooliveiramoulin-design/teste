// Help Farm — site próprio (helpfarm.cloud). Serve os arquivos da branch helpfarm-site do repositório.
// Binding de serviço HC → worker helpcure-site (área do investidor, gerencial e contador de visitas).
const RAW = "https://raw.githubusercontent.com/fabiooliveiramoulin-design/teste/helpfarm-site";
const TYPES = { html: "text/html; charset=utf-8", css: "text/css; charset=utf-8", js: "application/javascript; charset=utf-8", svg: "image/svg+xml", webp: "image/webp", jpg: "image/jpeg", jpeg: "image/jpeg", png: "image/png", mp4: "video/mp4", txt: "text/plain; charset=utf-8", xml: "application/xml", json: "application/json", ico: "image/x-icon" };
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.hostname === "www.helpfarm.cloud") return Response.redirect("https://helpfarm.cloud" + url.pathname + url.search, 301);
    let p = decodeURIComponent(url.pathname);
    if (p.includes("..") || p.startsWith("/priv/") || p.startsWith("/.")) return new Response("Not found", { status: 404 });
    // Área do investidor, gerencial e contador de visitas: atendidos pelo worker helpcure-site (códigos, cadastro e documentos cifrados).
    if (p === "/area-investidor" || p.startsWith("/area-investidor/")) return Response.redirect(url.origin + "/helpfarm/area-investidor" + p.slice("/area-investidor".length) + url.search, 302);
    if (p === "/helpfarm/area-investidor" || p.startsWith("/helpfarm/area-investidor/") || p.startsWith("/helpfarm/api/") || p === "/helpfarm/gerencial" || p.startsWith("/helpfarm/gerencial/")) return env.HC.fetch(req);
    // Demais endereços /helpfarm/... (links da área do investidor): páginas vão para a raiz; arquivos são servidos da raiz.
    if (p === "/helpfarm" || p.startsWith("/helpfarm/")) {
      const q = p.slice("/helpfarm".length) || "/";
      if (q.endsWith("/") || q.endsWith(".html")) return Response.redirect(url.origin + q + url.search, 301);
      p = q;
    }
    if (p.endsWith("/")) p += "index.html";
    else if (!/\.[a-z0-9]+$/i.test(p)) return Response.redirect(url.origin + p + ".html" + url.search, 301);
    const hdr = {}; const rg = req.headers.get("range"); if (rg) hdr.range = rg;
    const r = await fetch(RAW + p, { headers: hdr, cf: { cacheTtl: 300, cacheEverything: !rg } });
    if (!r.ok && r.status !== 206) return new Response("Not found", { status: 404 });
    const ext = p.split(".").pop().toLowerCase();
    const h = new Headers({ "content-type": TYPES[ext] || "application/octet-stream", "cache-control": ext === "html" ? "public, max-age=60" : "public, max-age=86400", "accept-ranges": "bytes", "x-content-type-options": "nosniff" });
    for (const k of ["content-length", "content-range"]) if (r.headers.get(k)) h.set(k, r.headers.get(k));
    return new Response(r.body, { status: r.status, headers: h });
  },
};
