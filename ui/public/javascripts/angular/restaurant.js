angular.module('restaurant', [

])
.controller('restaurantListCtrl', ['$http', '$scope', 'SERVER_URL', function($http, $scope, serverURL){
	$scope.restaurants = [];
	/*
		{
			id: 1,
			name: 'KFC',
			address: '2-25-6 Asakusa, Taito-ku, Tokyo',
			email: 'info@kfc.co.jp',
			tags: ['chicken', 'fried', 'xmas'],
			menus: [
				{
					name: 'XMAS bucket',
					price: 800,
					currency: 'JPY',
					tags: ['xmas', 'family'],
					images: ['test image url']
				}
			]
		},
		{
			id: 2,
			name: 'KFC',
			address: '2-25-6 Asakusa, Taito-ku, Tokyo',
			email: 'info@kfc.co.jp',
			tags: ['chicken', 'fried', 'xmas'],
			menus: [
				{
					name: 'XMAS bucket',
					price: 800,
					currency: 'JPY',
					tags: ['xmas', 'family'],
					images: ['test image url']
				},
				{
					name: 'XMAS bucket2',
					price: 800,
					currency: 'JPY',
					tags: ['xmas', 'family'],
					images: ['test image url']
				}
			]
		}
	];
	*/
	var req = {
		method: 'GET',
		url: serverURL + '/restaurants',
		headers: {
			'Content-Type': 'application/json',
		},
	};

	$http(req).success(function(data){
			$scope.restaurants = data.items;
	});
}]);