---
layout: single
classes: wide
author_profile: false
title: "Verifica opera"
description: "Chi e' il proprietario di questa opera."
noindex: true
ref: verifica
permalink: /verifica/
---
<div id="vf" data-json="{{ '/assets/data/proprietari.json' | relative_url }}" data-img="{{ '/assets/images/prodotti/' | relative_url }}" data-shop="{{ '/negozio/' | relative_url }}" data-contact="{{ '/contatti/' | relative_url }}" data-l='{"nf":"Opera non trovata. Controlla il QR code.","own":"Proprietario","col":"Collezione","art":"Artista","dt":"Data acquisto","tx":"Registro / transazione","sale":"In vendita a","nosale":"Non in vendita","offer":"Fai un\u0027offerta","buy":"Vedi la scheda","note":"Chiunque pu\u00f2 copiare l\u0027immagine, ma il proprietario \u00e8 solo quello indicato qui. Il QR code sull\u0027opera porta a questa pagina."}'>
  <p>Caricamento...</p>
</div>
<script>
(function(){
  var el=document.getElementById('vf'), L=JSON.parse(el.getAttribute('data-l'));
  var id=(new URLSearchParams(location.search).get('id')||'').replace(/[^a-z0-9-]/gi,'');
  function row(k,v){var p=document.createElement('p');var b=document.createElement('b');b.textContent=k+': ';p.appendChild(b);p.appendChild(document.createTextNode(v));return p;}
  el.textContent='';
  fetch(el.getAttribute('data-json')).then(function(r){return r.json();}).then(function(d){
    var o=d[id]; if(!o){el.textContent=L.nf;return;}
    var h=document.createElement('h2');h.textContent=o.opera;el.appendChild(h);
    var im=document.createElement('img');im.src=el.getAttribute('data-img')+id+'.webp';im.alt=o.opera;im.style.maxWidth='420px';im.style.width='100%';im.style.imageRendering='pixelated';el.appendChild(im);
    el.appendChild(row(L.col,o.collezione));el.appendChild(row(L.art,o.artista));
    el.appendChild(row(L.own,o.proprietario));el.appendChild(row(L.dt,o.data));
    if(o.tx)el.appendChild(row(L.tx,o.tx));
    el.appendChild(row(o.in_vendita?L.sale:L.nosale,o.in_vendita?o.prezzo:''));
    var a=document.createElement('a');a.className='btn btn--primary';a.textContent=L.offer;a.href=el.getAttribute('data-contact')+'?oggetto='+encodeURIComponent('Offerta '+id);el.appendChild(a);
    var n=document.createElement('p');n.style.marginTop='1rem';n.textContent=L.note;el.appendChild(n);
  }).catch(function(){el.textContent=L.nf;});
})();
</script>
