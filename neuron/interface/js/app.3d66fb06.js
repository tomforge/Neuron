(function(t){function e(e){for(var n,l,i=e[0],o=e[1],c=e[2],d=0,p=[];d<i.length;d++)l=i[d],r[l]&&p.push(r[l][0]),r[l]=0;for(n in o)Object.prototype.hasOwnProperty.call(o,n)&&(t[n]=o[n]);u&&u(e);while(p.length)p.shift()();return s.push.apply(s,c||[]),a()}function a(){for(var t,e=0;e<s.length;e++){for(var a=s[e],n=!0,i=1;i<a.length;i++){var o=a[i];0!==r[o]&&(n=!1)}n&&(s.splice(e--,1),t=l(l.s=a[0]))}return t}var n={},r={1:0},s=[];function l(e){if(n[e])return n[e].exports;var a=n[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,l),a.l=!0,a.exports}l.m=t,l.c=n,l.d=function(t,e,a){l.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},l.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},l.t=function(t,e){if(1&e&&(t=l(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(l.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)l.d(a,n,function(e){return t[e]}.bind(null,n));return a},l.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return l.d(e,"a",e),e},l.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},l.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],o=i.push.bind(i);i.push=e,i=i.slice();for(var c=0;c<i.length;c++)e(i[c]);var u=o;s.push([4,0]),a()})({4:function(t,e,a){t.exports=a("Vtdi")},FW5X:function(t,e,a){},GE1n:function(t,e,a){"use strict";var n=a("VVOC"),r=a.n(n);r.a},VVOC:function(t,e,a){},Vtdi:function(t,e,a){"use strict";a.r(e);a("VRzm");var n=a("Kw5r"),r=a("zlta"),s=a.n(r);a("v0CA");n["a"].use(s.a,{});var l=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-app",{attrs:{id:"inspire",dark:""}},[a("v-system-bar",{attrs:{status:"",app:"","lights-out":""}},[a("v-spacer"),a("span",{staticClass:"headline text-xs-center"},[t._v("neuron")]),a("v-spacer")],1),a("v-toolbar",{attrs:{color:"grey darken-3",dense:"",fixed:"","clipped-left":"",app:""}},[a("v-toolbar-title",{staticClass:"ml-3"}),a("v-spacer"),a("v-toolbar-items",[a("v-tabs",{attrs:{"fixed-tabs":"",color:"transparent"}},t._l(t.mainViews,function(e){return a("v-tab",{key:e.text,attrs:{to:e.link}},[t._v(t._s(e.text))])}))],1),a("v-spacer"),a("v-menu",{attrs:{bottom:"",left:"","offset-y":""}},[a("v-btn",{attrs:{slot:"activator",icon:""},slot:"activator"},[a("v-icon",[t._v("settings")])],1),a("v-list",t._l(t.mainViews,function(e){return a("router-link",{key:e.text,attrs:{to:e.link,tag:"v-list-tile"}},[a("v-list-tile-content",[a("v-list-tile-title",[t._v(t._s(e.text))])],1)],1)}))],1),a("v-menu",{attrs:{bottom:"",left:"","offset-y":""}},[a("v-btn",{attrs:{slot:"activator",icon:""},slot:"activator"},[a("v-icon",[t._v("help_outline")])],1),a("v-list",[a("router-link",{attrs:{to:"/about",tag:"v-list-tile"}},[a("v-list-tile-content",[a("v-list-tile-title",[t._v("About")])],1)],1),a("router-link",{attrs:{to:"/faq",tag:"v-list-tile"}},[a("v-list-tile-content",[a("v-list-tile-title",[t._v("FAQ")])],1)],1)],1)],1)],1),a("v-content",{staticStyle:{"background-color":"#212121"}},[a("router-view")],1)],1)},i=[],o={name:"App",data:function(){return{drawer:!0,mainViews:[{link:"/draw",text:"DRAW"},{link:"/run",text:"RUN"},{link:"/visualize",text:"VISUALIZE"}]}}},c=o,u=a("KHd+"),d=Object(u["a"])(c,l,i,!1,null,null,null),p=d.exports,f=a("jE9Z"),h=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-layout",{attrs:{"justify-center":"","align-start":""}},[a("v-flex",{staticClass:"text-xs-center",attrs:{shrink:""}},[a("h1",{staticClass:"display-4"},[t._v("neuron")]),a("p",{staticClass:"headline"},[t._v("v1.0.0-alpha")]),a("v-btn",{attrs:{depressed:"",href:"https://github.com/tomforge/neuron",target:"_blank"}},[a("v-icon",{attrs:{left:"",large:""}},[t._v("fa-github")]),t._v("\n      View on Github\n    ")],1),a("v-btn",{attrs:{depressed:"",href:"https://github.com/tomforge/neuron/blob/master/LICENSE",target:"_blank"}},[t._v("\n      LICENSE\n    ")])],1)],1)},v=[],g={},m=Object(u["a"])(g,h,v,!1,null,null,null),y=m.exports,b=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-container",{attrs:{fluid:"","fill-height":""}},[a("v-navigation-drawer",{staticClass:"pa-0 noscroll left-pane-style",attrs:{clipped:"",app:"",permanent:""},model:{value:t.drawer,callback:function(e){t.drawer=e},expression:"drawer"}},[a("v-layout",{attrs:{column:"","fill-height":""}},[a("v-flex",[a("v-tabs",{attrs:{"slider-color":"grey darken-4"}},[a("div",{staticClass:"attr-selection",staticStyle:{width:"100%",height:"100%"}},[a("v-tab",{attrs:{"active-class":"grey darken-3"}},[t._v("Add Nodes")]),a("v-tab",{attrs:{"active-class":"grey darken-3"}},[t._v("LOREM")]),a("v-tab",{attrs:{"active-class":"grey darken-3"}},[t._v("IPSUM")])],1)])],1),a("v-flex",{staticClass:"panel-style",staticStyle:{"min-height":"0"},attrs:{xs8:""}},[a("v-card",{attrs:{id:"nodes-panel",height:"100%"}},[a("v-layout",{attrs:{column:"","fill-height":""}},[a("v-flex",{staticClass:"shrink"},[a("v-text-field",{staticClass:"px-3 pb-0 pt-1 body-1",attrs:{"append-icon-cb":function(){},placeholder:"Search nodes","single-line":"","append-icon":"search",color:"white","hide-details":""},model:{value:t.searchStr,callback:function(e){t.searchStr=e},expression:"searchStr"}})],1),a("v-flex",{staticClass:"scroll"},[a("v-list",[t._l(t.filteredNodeTypes,function(e){return[a("v-menu",{key:e.type,attrs:{"open-on-hover":"","open-delay":"200","close-delay":"0",right:"","offset-x":"","full-width":"","close-on-content-click":!1}},[a("v-list-tile",{attrs:{slot:"activator",color:"grey lighten-1"},on:{click:function(a){t.addNode(e)}},slot:"activator"},[a("v-list-tile-content",[a("v-list-tile-title",{staticClass:"text-xs-center body-2",domProps:{innerHTML:t._s(t.$options.filters.highlight(e.type,t.searchStr,"white"))}},[t._v("\n                                                    "+t._s(e.type)+"\n                                                ")])],1)],1),a("v-card",{staticClass:"scroll",attrs:{flat:"",color:"grey darken-2",height:"500px",width:"750px"}},[a("v-card-title",[a("span",{staticClass:"headline"},[t._v(t._s(e.type))])]),a("v-card-text",[a("pre",[t._v(t._s(e.doc))])])],1)],1)]})],2)],1)],1)],1)],1),a("v-flex",{staticClass:"panel-style",staticStyle:{"min-height":"0"},attrs:{xs4:""}},[a("v-card",{staticClass:"elevation-5 grey--text text--lighten-2",attrs:{height:"100%"}},[a("v-layout",{attrs:{column:"","fill-height":""}},[a("v-flex",{staticClass:"shrink"},[a("v-card-title",{staticClass:"justify-center subheading pa-1 attr-selection"},[a("b",[t._v("Selection:")]),t._v("  "),a("em",{staticStyle:{color:"#F4FF81"}},[t._v(t._s(null===t.selectedNode?"NIL":t.selectedNode.type))])])],1),a("v-flex",{staticClass:"scroll"},[null!==t.selectedNode?a("v-data-table",{attrs:{items:Object.entries(t.selectedNode.params),"hide-actions":"","hide-headers":""},scopedSlots:t._u([{key:"items",fn:function(e){return[a("tr",{attrs:{id:"attr-row"}},[a("th",{staticClass:"text-xs-center"},[t._v(" "+t._s(t._f("titleCase")(e.item[0])))]),a("td",{staticClass:"pa-0"},[t._v(":")]),a("td",{attrs:{width:"100%"}},[a("v-edit-dialog",{attrs:{"return-value":t.selectedNode.params[e.item[0]],lazy:""},on:{"update:returnValue":function(a){t.$set(t.selectedNode.params,e.item[0],a)}}},[a("span",{staticClass:"text-xs-center"},[t._v(t._s(e.item[1]))]),a("v-text-field",{attrs:{slot:"input",label:"Edit","single-line":""},slot:"input",model:{value:t.selectedNode.params[e.item[0]],callback:function(a){t.$set(t.selectedNode.params,e.item[0],a)},expression:"selectedNode.params[props.item[0]]"}})],1)],1)])]}}])}):t._e(),null==t.selectedNode?a("span",{staticClass:"justify-center"},[a("em",{staticClass:"text-xs-center",staticStyle:{color:"#FFFFFF"}},[t._v("No data available.")])]):t._e()],1)],1)],1)],1)],1)],1),a("svg",[a("g")])],1)},_=[],w=(a("pIFo"),a("f3/d"),a("rGqo"),a("Vd3H"),a("Oyvg"),a("OG14"),a("yT7P")),x=a("VphZ"),k=a("EiaH"),C=a("L2JU"),S={name:"Draw",data:function(){return{drawer:!0,graph:"",nodes:[],edges:[],nodeCounter:0,searchStr:"",selectedNode:null}},computed:Object(w["a"])({},Object(C["b"])({nodeTypes:"nodeTypes",wsConnected:"wsConnected"}),{filteredNodeTypes:function(){var t=this;return this.searchStr?this.nodeTypes.filter(function(e){return-1!==e.type.search(new RegExp("\\b"+t.searchStr,"i"))}):this.nodeTypes}}),mounted:function(){this.nodeTypes.length||this.$store.commit("emit",["API_get_node_meta",""]),this.graphEditor()},methods:{graphEditor:function(){function t(){return(new k["graphlib"].Graph).setGraph({nodesep:30,ranksep:150,rankdir:"LR",marginx:20,marginy:20})}this.graph=t();var e=this.graph,a=this;function n(){e=t(),h(),a.nodes.sort(),a.nodes.forEach(function(t){"host"==t.type?e.setNode(t.name,{labelType:"html",label:t.name,class:"host",rx:5,ry:5,width:150}):e.setNode(t.name,{labelType:"html",label:t.name,class:"comp",rx:5,ry:5,width:150})}),a.edges.forEach(function(t){e.setEdge(t.source,t.target,{label:"",labelStyle:"fill: #FFFFFF",arrowhead:"vee",arrowheadStyle:"fill: #a5a5a5",style:"stroke: #a5a5a5; stroke-dasharray: 5, 5;",lineInterpolate:"bundle"})}),v()}var r=null,s=null,l=null,i=null,o=null,c=null,u=null,d=null,p=!0,f=null;function h(){i=null,o=null,l=null,u=null,d=null,p=!0,f=null}function v(){var t=new k["render"],g=x["c"]("svg"),m=g.select("g");function y(t){t.append("svg:defs").append("svg:marker").attr("id","end-arrow").attr("viewBox","0 0 10 10").attr("refX",9).attr("refY",5).attr("markerUnits","strokeWidth").attr("markerWidth",8).attr("markerHeight",6).attr("orient","auto").append("svg:path").attr("d","M 0 0 L 10 5 L 0 10 L 4 5 z").style("stroke-width",4).style("stroke-dasharray","1,0").attr("fill","#a5a5a5");var e=x["c"]("svg").selectAll("defs"),a=e.append("filter").attr("id","drop_shadow").attr("height","130%");a.append("feGaussianBlur").attr("in","SourceAlpha").attr("stdDeviation",5).attr("result","blur"),a.append("feOffset").attr("in","blur").attr("dx",2).attr("dy",2).attr("result","offsetBlur");var n=a.append("feSpecularLighting").attr("in","blur").attr("surfaceScale","5").attr("specularConstant","0.75").attr("specularExponent","20").attr("lighting-color","#73A0D1").attr("result","specOut");n.append("fePointLight").attr("x","-5000").attr("y","-10000").attr("z","20000"),a.append("feComposite").attr("in","specOut").attr("in2","SourceAlpha").attr("operator","in").attr("result","specOut"),a.append("feComposite").attr("in","SourceGraphic").attr("in2","specOut").attr("operator","arithmetic").attr("k1","0").attr("k2","1").attr("k3","1").attr("k4","0").attr("result","litPaint"),a.append("feOffset").attr("in","litPaint").attr("dx",-4).attr("dy",-4).attr("result","litPaint");var r=a.append("feMerge");r.append("feMergeNode").attr("in","offsetBlur"),r.append("feMergeNode").attr("in","litPaint")}t(m,e),y(g),x["d"]("svg g.node").on("mouseover",function(t){i&&t!==i&&(f||(f=x["c"](this).attr("transform"),x["c"](this).attr("transform",f+" scale(1.2)")))}).on("mouseout",function(t){i&&(f&&(x["c"](this).attr("transform",f),f=null),t===i&&(p=!1))}).on("mousedown",function(t){g.on(".zoom",null),console.log("node mousedown"),i=t,c=e.node(t),u=c.x+c.width/2,d=c.y,b.style("marker-end","url(#end-arrow)").attr("d","M"+u+","+d+"L"+u+","+d)}).on("mouseup",function(t){if(i){if(g.call(w),b.classed("hidden",!0).style("marker-end",""),o=t,o===i)return o!==r&&(r=o,a.selectedNode=a.nodes.filter(function(t){return t.name===r})[0]),s=null,void h();var n=e.edge(i,o);n||(e.setEdge(i,o,{label:"",labelStyle:"fill: #FFFFFF",arrowhead:"vee",arrowheadStyle:"fill: #a5a5a5",style:"stroke: #a5a5a5; stroke-dasharray: 5, 5;",lineInterpolate:"bundle"}),a.edges.push({source:i,target:o})),v()}}),x["d"](".edgePath, .edgeLabel").on("mouseover",function(t){var e=x["c"](this).attr("class");"edgeLabel"===e?f||(f=x["c"](this).attr("transform"),x["c"](this).attr("transform",f+" scale(1.2)")):"edgePath"===e&&x["c"](this).select(".path").transition().duration(25).style("stroke-width","8")}).on("mouseout",function(t){var e=x["c"](this).attr("class");"edgeLabel"===e?f&&(x["c"](this).attr("transform",f),f=null):x["c"](this).select(".path").transition().duration(50).style("stroke-width","4")}).on("click",function(t){console.log("clicked edge: "+JSON.stringify(e.edge(t))),l=t,l!==s&&(s=l),r=null}),x["c"]("body").on("keydown",function(){46===x["a"].keyCode&&(r?(a.nodes=a.nodes.filter(function(t){return t.name!==r}),a.edges=a.edges.filter(function(t){return t.source!==r&&t.target!==r}),r=null,a.selectedNode=null):s&&(a.edges=a.edges.filter(function(t){return t.source!==s.v||t.target!==s.w}),s=null),console.log("nodes: "+JSON.stringify(a.nodes)),console.log("edges: "+JSON.stringify(a.edges)),n())})}function g(){i&&b.classed("hidden",p).attr("d","M"+(u+_.x)*_.scale+","+(d+_.y)*_.scale+"L"+x["b"](this)[0]+","+x["b"](this)[1])}function m(){i&&b.classed("hidden",!0).style("marker-end",""),y.classed("active",!1),h()}n();var y=x["c"]("svg"),b=y.append("svg:path").attr("class","link dragline hidden").attr("marker-mid","").attr("d","M0,0L0,0"),_={x:0,y:0,scale:1},w=x["e"]().scaleExtent([0,1/0]).on("zoom",function(){_.x=x["a"].transform.x,_.y=x["a"].transform.y,_.scale=x["a"].transform.k,y.select("g").attr("transform",x["a"].transform)});y.call(w),y.on("mousemove",g).on("mouseup",m)},addNode:function(t){this.nodes.push({id:++this.nodeCounter,type:t.type,name:t.type+"<br/> ID: "+this.nodeCounter,params:t.params}),this.graphEditor()}},filters:{highlight:function(t,e,a){var n=new RegExp(e,"i");return t.replace(n,function(t){return'<span style="color:'+a+'">'+t+"</span>"})},titleCase:function(t){return t?t.replace(/\w\S*/g,function(t){return t.charAt(0).toUpperCase()+t.substr(1).toLowerCase()}):""}}},E=S,O=(a("hCY1"),a("GE1n"),Object(u["a"])(E,b,_,!1,null,"558b40be",null)),N=O.exports,T=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-container",{attrs:{fluid:"","fill-height":""}},[a("v-layout",{attrs:{"align-center":"","justify-center":""}},[a("v-flex",{attrs:{shrink:""}},[a("h1",[t._v("Run page")]),a("v-btn",[t._v("Upload training data")])],1)],1)],1)},F=[],j={},L=Object(u["a"])(j,T,F,!1,null,null,null),M=L.exports,P=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-container",{attrs:{fluid:"","fill-height":""}},[a("v-layout",{attrs:{"align-center":"","justify-center":""}},[a("v-flex",{attrs:{shrink:""}},[a("h1",[t._v("Visualize page")]),a("p",[t._v("View training statistics")])])],1)],1)},A=[],V={},z=Object(u["a"])(V,P,A,!1,null,null,null),I=z.exports;n["a"].use(f["a"]);var G=new f["a"]({routes:[{path:"/",redirect:"/draw"},{path:"/about",name:"about",component:y},{path:"/draw",name:"draw",component:N},{path:"/run",name:"run",component:M},{path:"/visualize",name:"visualize",component:I},{path:"*",redirect:"/draw"}]}),$=a("k5N+");function D(){var t="ws://"+location.host+"/ws",e="WebSocket"in window?new WebSocket(t):"MozWebSocket"in window?new MozWebSocket(t):null;return function(t){e&&(e.onopen=function(){return t.commit("SOCKET_CONNECT")},e.onclose=function(){return t.commit("SOCKET_DISCONNECT")},e.onmessage=function(e){return t.commit("SOCKET_HANDLE_MESSAGE",JSON.parse(e.data))},t.subscribe(function(t){if("emit"===t.type){var a=JSON.stringify(t.payload);e.readyState?e.send(a):setTimeout(function(){return e.send(a)},500)}}))}}n["a"].use(C["a"]);var R=D(),W=new C["a"].Store({state:{wsConnected:!1,wsPayload:"",nodeTypes:[]},mutations:{SOCKET_CONNECT:function(t){t.wsConnected=!0},SOCKET_DISCONNECT:function(t){t.wsConnected=!1},SOCKET_HANDLE_MESSAGE:function(t,e){var a=Object($["a"])(e,2),n=a[0],r=a[1];"RES_get_node_meta"===n&&(t.nodeTypes=r)},emit:function(t,e){}},actions:{},plugins:[R]});a("fxB9");n["a"].config.productionTip=!1,new n["a"]({router:G,store:W,render:function(t){return t(p)}}).$mount("#app")},hCY1:function(t,e,a){"use strict";var n=a("FW5X"),r=a.n(n);r.a}});
//# sourceMappingURL=app.3d66fb06.js.map