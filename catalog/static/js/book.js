(function() {
	var qrcode = new QRious({
		element: document.getElementById("qrcode"),
		background: '#332f35',
		foregroundAlpha: 0.9,
		foreground: '#eaeaea',
		//level: 'H',
		//padding: 0,
		size: 180,
		value: qr_link
	});
})();
//         fr     bc
// light #eaeaea #332f35
// dark #332f35 #1f1c23