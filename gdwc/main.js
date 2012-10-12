$.get(chrome.extension.getURL("statusbar.html"), {}, function(data) {$('body').append(data);}, 'html');
chrome.extension.sendRequest({}, function(response) {});

$(document).ready(function(){
	countWords();
});

function countWords() {
	var number = 0;
	$('span.kix-lineview-text-block').each(function(i, obj){
		number += $(obj).text().split(/\s+/).length;
	});
	$('span#GDWC_wordsTotal').text(number + ' total words');
	timeout = setTimeout('countWords()', 5000);
}