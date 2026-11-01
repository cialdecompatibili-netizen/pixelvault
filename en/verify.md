---
layout: single
classes: wide
author_profile: false
title: "Verify artwork"
description: "Who owns this artwork."
noindex: true
ref: verifica
lang: en
locale: en
tr: tradotto
permalink: /en/verify/
---
<div id="vf" data-json="{{ '/assets/data/proprietari.json' | relative_url }}" data-img="{{ '/assets/images/prodotti/' | relative_url }}" data-shop="{{ '/en/shop/' | relative_url }}" data-contact="{{ '/en/contact/' | relative_url }}" data-l='{"nf":"Artwork not found. Check the QR code.","own":"Owner","col":"Collection","art":"Artist","dt":"Purchase date","tx":"Registry / transaction","sale":"For sale at","nosale":"Not for sale","offer":"Make an offer","buy":"See the page","note":"Anyone can copy the image, but the owner is only the one shown here. The QR code on the artwork leads to this page."}'>
  <p>Loading...</p>
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
    var a=document.createElement('a');a.className='btn btn--primary';a.textContent=L.offer;a.href=el.getAttribute('data-contact')+'?oggetto='+encodeURIComponent('Offer '+id);el.appendChild(a);
    var n=document.createElement('p');n.style.marginTop='1rem';n.textContent=L.note;el.appendChild(n);
  }).catch(function(){el.textContent=L.nf;});
})();
</script>
