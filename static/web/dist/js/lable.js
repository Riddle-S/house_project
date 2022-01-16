var bodyHeight = document.body.offsetHeight;
$(function() {
    //上半部分高度
    // $('.topItem').css('height', 0.6 * bodyHeight + "px");
    // //下半部分高度
    // $('.maxHeight').css('height', (0.4 * bodyHeight - 20) + "px");
    // //右侧滑动菜单高度
    // $('.swiper-container').css('height', 0.6 * bodyHeight - 141 + "px");
    //首页加载，第一次调用，获取产品列表及各地数据
    //获取默认农产品列表
    setTimeout(getGoodList(), 0);

    function getGoodList() {
        //绑定数据
        //激活滚动窗口
        var nMark = 0;

        function setSor() {
            nMark++;
            //alert(nMark);
            if (nMark == 5) {
                setTimeout(function() {
                    var swiper2 = new Swiper('.innerSw', {
                        scrollbar: '.innerSc',
                        direction: 'vertical',
                        slidesPerView: 'auto',
                        mousewheelControl: true,
                        freeMode: true,
                        roundLengths: true,
                        noSwiping: false
                    });
                }, 300);
            }
        }
        //结束，已激活
    }
    //获取各地区数据


})
window.onresize = function() {
    window.location.reload();
}