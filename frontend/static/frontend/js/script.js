const search_button = document.getElementById('view_statistics_button');
const home_button = document.getElementById('home_button');

var current_url = window.location.href;
var base_url = current_url.substring(0, current_url.search("statistics")) + "statistics/";

search_button.addEventListener('click', event => {
	var provider_value = document.getElementById('select_provider_input').value;
	var date_from_value = document.getElementById('date_from_input').value;
	var date_to_value = document.getElementById('date_to_input').value;

	var input_url = provider_value + '/' + date_from_value + '/' + date_to_value;
	var target_url = base_url  + input_url;
	window.location.href = target_url;
});

home_button.addEventListener('click', event => {
	window.location.href = base_url;
});

const search_form = document.getElementById('search_form');

search_form.addEventListener('mouseover', event => {
	search_form.classList.remove("shadow-sm");
});

search_form.addEventListener('mouseout', event => {
	search_form.classList.add("shadow-sm");
});