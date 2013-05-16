(function($) {
    $(document).ready(function($) {
        // GENERAL VARIABLES
        var admin_url = '/admin/';
        var prefix = 'zotero-tag-content_type-object_id';
        var numFields = 133;
        
        
        // ORIGINAL SELECTORS
        var itemTypeLabel = 'label[for^="id_' + prefix + '"][for$="item_type"]';
        var itemTypeSelect = 'select[id^="id_' + prefix + '"][id$="item_type"]';
        var fieldSelect = 'select[id^="id_' + prefix + '"][id$="field"]';
        var deleteCheckbox = 'input[id^="id_' + prefix + '"][id$="DELETE"]';
        
        
        // DERIVED SELECTORS
        // Item types
        var itemTypeLabelAll = itemTypeLabel
        var itemTypeLabelFirst = itemTypeLabelAll + ':first';
        var itemTypeSelectAll = itemTypeSelect
        var itemTypeSelectFirst = itemTypeSelectAll + ':first';
        
        // Fields
        var fieldSelectAll = fieldSelect
        
        // Deletes
        var deleteCheckboxAll = deleteCheckbox
        var deleteCheckboxLast = deleteCheckboxAll + ':last';
        
        
        // STYLE
        // Add brs
        var addBrs = function() {
            $(itemTypeLabelFirst).before('<br/><br/>');
            $(itemTypeSelectFirst).after('<br/><br/>');
            $(deleteCheckboxAll).after('<br/>');
            $(deleteCheckboxLast).after('<br/><br/>');
        }
        addBrs();
        
        
        // BEHAVIOUR
        // Choose applicable fields
        var changeFields = function() {
            var itemTypeValueFirst = $(itemTypeSelectFirst).val();
            if(itemTypeValueFirst == "")
                itemTypeValueFirst = "1";
            $.getJSON(admin_url + "zotero/itemtype/" + itemTypeValueFirst + "/fields", function(data) {
                // Show all fields
                var fields = fieldSelectAll + " option";
                $(fields).show();
                
                // Get data
                var applicableFields = data;
                
                // Hide non applicable fields
                for(var i = 1; i <= numFields; i++)
                {
                    if(applicableFields.indexOf(i) == -1)
                    {
                        var nonApplicableOptions = fields + "[value='" + i + "']";
                        $(nonApplicableOptions).hide();
                    }
                }
            })
        }
        
        // Set item_type's values
        var setItemTypesValues = function() {
            $(itemTypeSelectAll).val($(itemTypeSelectFirst).val());
        }
        
        // Hide other item_type selectors and labels
        var hideItemType = function() {
            $(itemTypeSelectAll).hide();
            $(itemTypeSelectFirst).show();
            $(itemTypeLabelAll).hide();
            $(itemTypeLabelFirst).show();
        }
        
        // All actions
        var performActions = function() {
            hideItemType();
            setItemTypesValues();
            changeFields();
        }
        performActions();
        
        $(itemTypeSelectFirst).change(function(){
            setItemTypesValues();
            changeFields();
        });
    });
})(jQuery);
