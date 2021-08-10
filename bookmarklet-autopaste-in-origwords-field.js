javascript: (function()%7B var newSS, styles='* %7B background: white ! important; color: black !important %7D :link, :link * %7B color: #0000EE !important %7D :visited, :visited * %7B color: #551A8B !important %7D'; if(document.createStyleSheet) %7B document.createStyleSheet("javascript:'"+styles+"'"); %7D else %7B newSS=document.createElement('link'); newSS.rel='stylesheet'; newSS.href='data:text/css,'+escape(styles); document.getElementsByTagName("head")[0].appendChild(newSS); %7D %7D )();


javascript:(function(){var newSS, styles=' [data-test] { font-family: "Times"; font-size: 2rem; }'; if(document.createStyleSheet) { document.createStyleSheet("javascript:'"+styles+"'"); } else { newSS=document.createElement('link'); newSS.rel='stylesheet'; newSS.href='data:text/css,'+escape(styles); document.getElementsByTagName("head")[0].appendChild(newSS); } })();

javascript:(function(){var whichField =  })();