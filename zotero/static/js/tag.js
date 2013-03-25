(function($) {
    $(document).ready(function($) {
         // you can now use jquery / javascript here...
//         alert('It worked.');
//         $(".field-item_type").html("");
//         $(".field-item_type:last").html("");
//         $("p:last").hide();
//         $("p").toggle();
//         $("#id_zotero-tag-content_type-object_id-0-item_type").change(function(){alert($(this).val())});
//         $.get("http://127.0.0.1:8000/admin/zotero/itemtype/2/", function(data){
//                alert(data);
//            });
//         $.get("http://127.0.0.1:8000/admin/zotero/itemtype/2/", function(data){
//                var x = $("[selected]", data);
//                x.each(function(){alert($(this).text())})
//            });
//         var x = $("option:nth-child(11)")
//         x.hide()
//         x.show()
        var item_type_selector = $("#id_zotero-tag-content_type-object_id-0-item_type");
        item_type_selector.change(function(){
            $.get("/admin/zotero/itemtype/" + item_type_selector.val() + "/", function(data){
                var applicable_fields = $("[selected]", data);
                var first = [applicable_fields.pop()];
                applicable_fields = first.
                var all_field_selectors = $("select:odd option");
//                all_field_selectors.hide();
//                applicable_fields.filter(function(index){
//                    alert($(this).html()+" - "+index)
//                });
//                all_field_selectors.filter(function(index){
//                    alert($(this).html()+" - "+index)
//                });
                debugger;
                var field_selectors;
                applicable_fields.each(function(){
                    //alert($(this).html()+" - "+$(this).val());
                    var val = $(this).val() + 1;
                    field_selectors = $("select:odd option:nth-child(" + val + ")");
//                    debugger;
                    //alert(field_selectors.html());
                    field_selectors.show();
                });
//                all_field_selectors.each(function(){
//                    alert($(this).html());
//                });
//                alert(all_field_selectors.html());
            });
        });
    });
})(django.jQuery);
