(function($) {
    $(document).ready(function($) {
        var tabularInlineZotero = ".inline-group[id^='zotero-tag'] .tabular.inline-related"
        var fieldItemType = tabularInlineZotero + " .field-item_type"
        var fieldField = tabularInlineZotero + " .field-field"
        
        //Applicable fields
        var firstItemTypeSelector = fieldItemType + " select:first";
        var changeFields = function() {
            $.get("/admin/zotero/itemtype/" + $(firstItemTypeSelector).val() + "/", function(data) {
                //Show all fields
                var fields = fieldField + " select option";
                $(fields).show();
                
                //Get data
                var allFieldsData = $("select:first option", data);
                var applicableFieldsData = $("select option[selected]", data);
                
                //Collect non applicable fields
                var applicableIndexes = [];
                for(var i = 0; i < applicableFieldsData.length; i++)
                {
                    var f = $(applicableFieldsData[i]);
                    var val = f.attr("value");
                        if(val == "")
                            val = "0";
                    applicableIndexes = applicableIndexes.concat(parseInt(val));
                }
                var nonApplicableIndexes = [];
                for(var i = 0; i < allFieldsData.length; i++)
                {
                    if(applicableIndexes.indexOf(i) == -1)
                        nonApplicableIndexes = nonApplicableIndexes.concat(i);
                }
                
                //Hide non applicable fields
                for(var i = 0; i < nonApplicableIndexes.length; i++)
                {
                    var val = parseInt(nonApplicableIndexes[i]) + 1;
                    var nonApplicableOptions = fields + ":nth-child(" + val + ")";
                    $(nonApplicableOptions).hide();
                }
            });
        }
        changeFields();
        $(firstItemTypeSelector).change(changeFields);
        
        //Hide other item_type selectors
        var len = $(fieldItemType).length
        if(len > 2)
        {
            var itemTypeSelectors = fieldItemType + " select";
            $(itemTypeSelectors).slice(1,len-1).hide();
            var itemTypeAdd = fieldItemType + " a";
            $(itemTypeAdd).slice(1,len-1).hide();
        }
    });
})(django.jQuery);
