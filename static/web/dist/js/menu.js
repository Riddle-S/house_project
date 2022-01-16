$(function(){
	//首页跳转单独写
	$('.aloneBut').on('click',function(){
		var url = $(this).attr('url');
		a(url);
	})
	//其他跳转按钮
	$('.treeview-menu li').click(function(){
		$('.treeview-menu .active').removeClass('active');
		$(this).addClass('active');
		var url = $(this).attr('url');
		a(url);
	});
	//页面跳转类
	function a(url){
		$('#mianFrame').attr('src',url);
	}
})