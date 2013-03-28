(function($) {
    $(document).ready(function($) {
        var tabularInlineZotero = "#zotero-tag-content_type-object_id-group .tabular.inline-related"
        var fieldItemType = tabularInlineZotero + " .field-item_type"
        var fieldField = tabularInlineZotero + " .field-field"
        
        var firstItemTypeSelector = fieldItemType + " select:first";
        var itemTypeSelectors = fieldItemType + " select";
        var addAnotherTag = tabularInlineZotero + " a[href='javascript:void(0)']";
        
        //Choose applicable fields
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
                
                //Listen to click events from "Add another Tag"
                $(addAnotherTag).click(performActions);
            });
        }
        
        //Set item_type's values
        var setItemTypesValues = function() {
            $(itemTypeSelectors).val($(firstItemTypeSelector).val());
        }
        
        //Hide other item_type selectors
        var hideItemType = function() {
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
//            hideItemType();
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
