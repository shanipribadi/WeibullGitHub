<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Bootstrap 3, from LayoutIt!</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">

	<!--link rel="stylesheet/less" href="less/bootstrap.less" type="text/css" /-->
	<!--link rel="stylesheet/less" href="less/responsive.less" type="text/css" /-->
	<!--script src="js/less-1.3.3.min.js"></script-->
	<!--append ‘#!watch’ to the browser URL, then refresh the page. -->
	
	<link href="/static/css/bootstrap.min.css" rel="stylesheet">
	<link href="/static/css/style.css" rel="stylesheet">

  <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
  <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
  <![endif]-->

  <!-- Fav and touch icons -->
  <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/static/img/apple-touch-icon-144-precomposed.png">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/static/img/apple-touch-icon-114-precomposed.png">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/static/img/apple-touch-icon-72-precomposed.png">
  <link rel="apple-touch-icon-precomposed" href="/static/img/apple-touch-icon-57-precomposed.png">
  <link rel="shortcut icon" href="/static/img/favicon.png">
  
	<script type="text/javascript" src="/static/js/jquery.min.js"></script>
	<script type="text/javascript" src="/static/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="/static/js/scripts.js"></script>
</head>

<body>
<div class="container">
	<div class="row clearfix">
		<div class="col-md-12 column">
			<h3 class="text-center">
				WEIBULL PARAMETER ESTIMATOR
			</h3>
			<p class="text-center">
				SELAMAT DATANG!
			</p>
			<div>
			<h3 class="text-center">
				Dalam halaman ini, anda akan menemukan alat bantu untuk perhitungan 3 buah parameter weibull yaitu parameter bentuk, parameter skala dan parameter lokasi. Untuk memulai, masukkan file dengan ekstensi .csv yang berisi data kegagalan.
			</div>
			<div>
			<h3 class="text-center">
				Hasilnya, anda akan mendapatkan grafik weibull dan ketiga parameter tersebut.
			</div>
			<div>
			<h3 class="text-center">
				SELAMAT MENCOBA!
			</div>
			
					<p class="help-block">
						Pilih salah satu metode input data
						1. Masukkan data kegagalan secara manual
					</p>

			<form method = "post" enctype="multipart/form-data" action= "/fitting" target ="_blank">
			<table border ="1">
			<thead>
				<tr>
					<th>Failure Time</th>
				</tr>
			</thead>	
				<tr>
					<td><textarea rows ="50" cols = "20" name ="inputdata"></textarea>
					<button type="submit" class="btn btn-default">Hitung</button>
				</tr>


			</table>
					
			</form>

					<p class="help-block">
						2. Masukkan data kegagalan dalam file dengan ekstensi .csv
					</p>

			<form role="form" method="post" enctype= "multipart/form-data" action="/fitting?upload=1" target="_blank">

				<div class="form-group">
					 <label for="exampleInputFile">File input</label><input type="file" name= "inputfile" id="exampleInputFile">

				</div>
				<button type="submit" class="btn btn-default">Hitung</button>
			
		</div>
	</div>
</div>
</body>
</html>
