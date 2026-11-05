# Help Farm — filme principal, fotos tiradas do filme e espaços dos vídeos explicativos em desenho.
import sys


def B():
    return sys.modules["__main__"]


def photo(src, alt, cls="ph"):
    return f'<img class="{cls}" src="img/f/{src}.webp" alt="{alt}" loading="lazy">'


def film(pg):
    return f'''<section class="filmsec" id="filme">
  <div class="wrap">
    <div class="head">{pg.t("O filme", "La película", "The film", "span", "eyebrow")}{pg.t("A sua fazenda é única. Veja em 3 minutos.", "Su establecimiento es único. Véalo en 3 minutos.", "Your farm is unique. See it in 3 minutes.", "h2")}</div>
    <div class="filmbox"><video controls playsinline preload="none" poster="video/helpfarm-filme-pt-poster.jpg"><source src="video/helpfarm-filme-pt.mp4" type="video/mp4"></video></div>
    {pg.t("Narração em português. Versões em espanhol e inglês em produção.", "Narración en portugués. Versiones en español e inglés en producción.", "Narrated in Portuguese. Spanish and English versions in production.", "p", "filmnote")}
  </div>
</section>'''


# esboço "desenho no papel" — mesmo traço para todas as páginas, com o tema no centro
DOODLE = {
    "home": '<path d="M70 150 q30-40 60 0 t60 0" /><rect x="60" y="150" width="140" height="44" rx="6"/><path d="M240 120 l40-30 40 30 v70 h-80z"/><path d="M360 170 c30-60 60 20 90-40 s50 10 70-20" class="acc"/><circle cx="520" cy="110" r="10" class="acc"/>',
    "movel": '<rect x="70" y="110" width="250" height="80" rx="10"/><rect x="320" y="128" width="80" height="62" rx="8"/><circle cx="130" cy="196" r="16"/><circle cx="350" cy="196" r="16"/><path d="M90 104 h200" /><path d="M430 80 l20-10 20 10 M440 60 h40" class="acc"/><path d="M450 90 v30" class="acc" stroke-dasharray="4 6"/>',
    "tec": '<path d="M60 190 h480 M60 190 V70"/><path d="M70 150 C140 120 180 165 250 145 S360 120 400 148" class="band"/><path d="M70 150 C140 120 180 165 250 145 S360 120 400 148"/><path d="M400 148 C430 160 460 190 520 200" class="acc" stroke-dasharray="7 6"/><circle cx="440" cy="168" r="9" class="acc"/>',
    "cert": '<path d="M80 80 l120-10 20 90 -110 20z"/><circle cx="330" cy="130" r="44"/><path d="M312 132 l12 12 24-26" class="acc"/><rect x="430" y="90" width="90" height="90" rx="6"/><path d="M445 105 h20v20h-20z M485 105 h20v20h-20z M445 145 h20v20h-20z M490 150 h10" />',
    "inv": '<path d="M70 190 h460"/><rect x="100" y="150" width="50" height="40"/><rect x="190" y="125" width="50" height="65"/><rect x="280" y="100" width="50" height="90"/><rect x="370" y="70" width="50" height="120" class="acc"/><path d="M110 120 L210 96 L300 76 L400 44" class="acc"/>',
}


def explainer(pg, key, title, dur, scenes):
    sc = "".join("<li>%s</li>" % pg.t(*s) for s in scenes)
    return f'''<div class="explain">
  <div class="ex-paper"><svg viewBox="0 0 600 240" aria-hidden="true"><g class="ink">{DOODLE[key]}</g><g class="pencil" transform="translate(470,170) rotate(-35)"><rect width="110" height="16" rx="3"/><path d="M110 0 l18 8 -18 8z"/></g></svg>
    <span class="ex-badge">{pg.t("Vídeo em desenho · em produção", "Video en dibujo · en producción", "Hand-drawn video · in production", "span")}</span></div>
  <div class="ex-text">
    {pg.t("Vídeo explicativo", "Video explicativo", "Explainer video", "span", "eyebrow")}
    {pg.t(*title, "h3")}
    <p class="ex-dur">{dur}</p>
    <ol class="ex-scenes">{sc}</ol>
  </div>
</div>'''
