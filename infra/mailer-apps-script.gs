// Help Cure — envio de e-mails do site (helpcure.com.py) pela conta fabio.moulin@helpcure.com.py.
// Chamado pelo worker "helpcure-site" do Cloudflare (segredos MAIL_URL e MAIL_KEY).
// Corpo JSON: {key, from, to, cc, replyTo, subject, text}
var KEY = "<MAIL_KEY — mesmo valor do segredo MAIL_KEY do worker>";
var REMETENTES = ["investidores@helpcure.com.py", "campanha@helpcure.com.py", "contato@helpcure.com.py", "privacidade@helpcure.com.py"];

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents);
    if (d.key !== KEY) return saida({ ok: false, erro: "chave" });
    if (!d.to || !d.subject || !d.text) return saida({ ok: false, erro: "campos" });
    var de = REMETENTES.indexOf(d.from) >= 0 ? d.from : "contato@helpcure.com.py";
    var aliases = GmailApp.getAliases();
    var opt = { name: "Help Cure", replyTo: d.replyTo || de };
    if (aliases.indexOf(de) >= 0) opt.from = de;
    if (d.cc) opt.cc = d.cc;
    GmailApp.sendEmail(d.to, d.subject, d.text, opt);
    return saida({ ok: true, from: opt.from || Session.getActiveUser().getEmail() });
  } catch (err) {
    return saida({ ok: false, erro: String(err).slice(0, 200) });
  }
}

function doGet() { return saida({ ok: true, servico: "helpcure-mailer" }); }

function saida(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

// Rode uma vez no editor para autorizar o envio e ver os aliases liberados.
function testar() { Logger.log(GmailApp.getAliases()); }
