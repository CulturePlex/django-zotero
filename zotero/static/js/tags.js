(function($) {
    $(document).ready(function($) {
        var tabularInlineZotero = "#zotero-tag-content_type-object_id-group .tabular.inline-related"
        var fieldItemType = tabularInlineZotero + " .field-item_type"
        var fieldField = tabularInlineZotero + " .field-field"
        
        var itemTypeSelectors = fieldItemType + " select";
        var firstItemTypeSelector = itemTypeSelectors + ":first";
        var firstItemTypeSelectedOption = firstItemTypeSelector + " option[selected]"
        
        var itemTypeSpanClass = "zotero-itemtype-text"
        var itemTypeSpan = fieldItemType + " span." + itemTypeSpanClass
        var firstItemTypeSpan = itemTypeSpan + ":first"
        
        //Choose applicable fields
        var changeFields = function() {
            var val = $(firstItemTypeSelector).val();
            if(val == "")
                val = "1";
            $.get("/admin/zotero/itemtype/" + val + "/", function(data) {
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
                    applicableIndexes = applicableIndexes.concat(parseInt(val));
//                        if(val == "")
//                            val = "0";
//                    applicableIndexes = applicableIndexes.concat(parseInt(val));
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
                    var nonApplicableOptions = fields + "[value='" + nonApplicableIndexes[i] + "']";
//                    var val = parseInt(nonApplicableIndexes[i]) + 1;
//                    var nonApplicableOptions = fields + ":nth-child(" + val + ")";
                    $(nonApplicableOptions).hide();
                }
                
                //Listen to click events from "Add another Tag"
                addAnotherTag = tabularInlineZotero + " a[href='javascript:void(0)']";
                $(addAnotherTag).click(performActions);
            })
        }
        
        //Add span
        var addSpan = function() {
            var span = "<span class=\"" + itemTypeSpanClass + "\"></span>"
            $(fieldItemType).append(span);
        }
        addSpan();
        
        //Set item_type's values
        var setItemTypesValues = function() {
            $(itemTypeSelectors).val($(firstItemTypeSelector).val());
            $(itemTypeSpan).text($(firstItemTypeSelectedOption).text())
        }
        
        //Hide first span and other item_type selectors
        var hideItemType = function() {
            $(itemTypeSpan).removeAttr('style')
            $(firstItemTypeSpan).hide()
            var len = $(fieldItemType).length
            if(len > 2)
            {
                $(itemTypeSelectors).slice(1,len-1).hide();
                var itemTypeAdd = fieldItemType + " a";
                $(itemTypeAdd).slice(1,len-1).hide();
            }
        }
        
        //All actions
        var performActions = function() {
            hideItemType();
            setItemTypesValues();
            changeFields();
        }
        
        performActions();
        $(firstItemTypeSelector).change(function(){
            setItemTypesValues();
            changeFields();
        });
    });
})(django.jQuery);
