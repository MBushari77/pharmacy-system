$(document).ready(function(){


});
function edit(x){
	location.href='/editproduct/' + x;
}
function del(x){
	if (confirm('هل تربد حزف هذا العنصر')) {
		location.href='/deleteproduct/' + x;
	}
}
function togglePopup(){
	document.getElementById("popup-1").classList.toggle("active");
}
function delFromList(x){
	$("#"+x).remove();
}

function clearCounters(){
	if (confirm('OK we will start counting again')) {
		location.href='/clearcounters'
	}
}
function delDeal(x){
	if (confirm('هل تم دفع الفاتورة')) {
		location.href='/paid/'+x
	}
}

function getDailyTotal(){
	let totalOfSelingPrices = document.querySelectorAll('#totalOfSelingPrices');
	let totalOfSelingPricesVal = 0;
	for(let i = 0; i < totalOfSelingPrices.length; i++){
		totalOfSelingPricesVal += Number(totalOfSelingPrices[i].textContent);
	}
	let grossList = document.querySelectorAll('#gross');
	let totalOfGrossing = 0;
	for(let i = 0; i < grossList.length; i++){
		totalOfGrossing += Number(grossList[i].textContent);
	}
	let listOfCuts = document.querySelectorAll('#cutsTotal');
	let totalMountOfCuts = 0;
	for(let i = 0; i < listOfCuts.length; i++){
		totalMountOfCuts += Number(listOfCuts[i].textContent)
	}
	// listOfTotals = document.querySelectorAll('#dailyTotal')
	// let totalMountOfDeals = 0;
	// let totalMountOfCuts = 0;
	// for(let i = 0; i < listOfTotals.length; i++){
	// 	totalMountOfDeals += Number(listOfTotals[i].textContent)
	// }
	document.getElementById('income').textContent = totalOfSelingPricesVal;
	document.getElementById('grossing').textContent = totalOfGrossing;
	document.getElementById('outcome').textContent = totalMountOfCuts;
	document.getElementById('inSafe').textContent = totalOfSelingPricesVal - totalMountOfCuts;
}

function confirmPassword(){
	if (document.getElementById('password1').value == document.getElementById('password2').value) {
		document.getElementById('notMatchesMsg').textContent = '';
		$('#regUser').click();
	}
	else{
		document.getElementById('notMatchesMsg').textContent = 'الرقم السري غير متطابق';
	}
}
let tak = document.querySelectorAll('.round');
for(let i = 0; i < tak.length; i++){
	tak[i].textContent = Number(tak[i].textContent).toFixed(1)
}
$('body').append('<button class="btn_logout btn btn-success">تسجيل الخروج<i class="icon-logout"></i></button>')

// get the prices
// for(let i = 0; i < x.children().length; i++){console.log(document.getElementById("ps"+x.children()[i].id).textContent)}
// get the number of pices
// for(let i = 0; i < x.children().length; i++){console.log(document.getElementById("pis"+x.children()[i].id).value)}
$('.btn_logout').click(function(){
	location.href = '/logout';
})