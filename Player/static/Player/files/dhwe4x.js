// Created by Dynamic HTML Editor V.4.3
function jsGetLayer(n){var o;if(isDom2)return document.getElementById(n);if(isNS)return document.layers[n];if(isIE)return document.all(n);if(o=eval('document.'+n))return o;return null;}
function jsGetPic(n){var d;if(isNS)if(d=document.layers['ldhe'+n]) return d.document.images[n];return jsGetLayer(n);}
function jsGetArray(s){return s.split(';');}
function jsCngPic(n,d,s,a){if(!a)return;var o;if(o=jsGetPic(n))if (a[s])o.src=a[s];a[d]=a[s];}
function jsShow(n,b){var o;if(o=jsGetLayer('ldhe'+n)){if(isNS)return(o.visibility=b?'show':'hide');else if(o.style)return(o.style.visibility=b?'inherit':'hidden');}}
function jsMove(n,l,t){var o;if(o=jsGetLayer('ldhe'+n)){if(isNS){o.left=l;o.top=t;}else if(o.style){o.style.left=l+'px';o.style.top=t+'px';}}}
function jsRoll(n,s,a){if(!a)return;var o;if(o=jsGetPic(n))if(a[s])o.src=a[s];}
function jsStop(n){var o;if(o=jsGetLayer(n)){o.stop();}}
function jsPlay(n){var o;if(o=jsGetLayer(n)){o.play();}}
function jsSetStatus(s){window.status=s;}
function jsSetStyle(n,cn){var o;if(o=jsGetLayer(n))o.className=cn;}
function jsLink(sl,st){if(!st)st="_self";window.open (sl,st);}
function jsComboLink(o){var v,i,sl,st;if(o){i=o.selectedIndex;if(i>0){v=o[i].value;if(v.length){v=v.split('[*]');jsLink(v[0],v[1]);}}}}
function jsFixZoom(g){var e=document.styleSheets;if(!e){return}for(var c=0;c<e.length;c++){var b=e[c].rules?e[c].rules:e[c].cssRules;if(!b){return}for(var d=0;d<b.length;d++){var f=b[d];if(f.style&&f.style.fontSize){if(f.style.fontSize.indexOf("px")!=-1){var a=parseInt(f.style.fontSize,10)/g;if(!isNaN(a)){f.style.fontSize=a+"px"}}}}}}
function jsCheckZoom(){var b=jsGetLayer("ldheCheckZoom");if(b&&b.style){b.style.display="block";var a=b.offsetWidth;b.style.display="none";if(a>0&&a!=9){jsFixZoom(a/9)}}};
