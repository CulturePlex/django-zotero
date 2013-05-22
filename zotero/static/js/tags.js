(function($) {
    $(document).ready(function($) {
        // GENERAL VARIABLES
        var prefix = "zotero-tag-content_type-object_id";
        var admin_url = "/admin/";
        var numFields = 133;
        
        
        // SELECTORS
        var container = "div." + prefix;
        var itemTypeAll = container + " td.field-item_type select";
        var itemTypeFirst = itemTypeAll + ":first";
        var fieldAll = container + " td.field-field select";
//        var delAll = container + " td.field-DELETE a";
        var idAll = container + " td.field-id"
        var add = container + " td a.add-row"
        
        
        // BEHAVIOUR
        // Choose applicable fields
        var changeFields = function() {
            var itemTypeValueFirst = $(itemTypeFirst).val();
            if(itemTypeValueFirst == "")
                itemTypeValueFirst = "1";
            $.getJSON(admin_url + "zotero/itemtype/" + itemTypeValueFirst + "/fields", function(data) {
                // Show all fields
                var fields = fieldAll + " option";
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
            $(itemTypeAll).val($(itemTypeFirst).val());
        }
        
        // Hide other item_type selectors and hidden fields
        var hideItemTypeAndId = function() {
            $(itemTypeAll).hide();
            $(itemTypeFirst).show();
            $(idAll).hide();
        }
        
        // All actions
        var performActions = function() {
            hideItemTypeAndId();
            setItemTypesValues();
            changeFields();
        }
        performActions();
        
        $(itemTypeFirst).change(function(){
            setItemTypesValues();
            changeFields();
        });
        
        
        // INLINES
        var formset = function() {
            var alternatingRows = function(row) {
                $(rows).not(".add-row").not(":hidden").removeClass("row1 row2")
                    .filter(":even").addClass("row1").end()
                    .filter(":odd").addClass("row2");
            }
            
            rows = container + " tbody tr";
            $(rows).formset({
                prefix: prefix,                    // The form prefix for your django formset
                formTemplate: null,                // The jQuery selection cloned to generate new form instances
                addText: "Add a tag",              // Text for the add link
                deleteText: "remove",              // Text for the delete link
                addCssClass: "add-row",            // CSS class applied to the add link
                deleteCssClass: "delete-row",      // CSS class applied to the delete link
                formCssClass: "dynamic-" + prefix, // CSS class applied to each form in a formset
                extraClasses: [],                  // Additional CSS classes, which will be applied to each form in turn
                emptyCssClass: "empty-form",
                removed: (function(row) {
                    alternatingRows(row);
                }),                                // Function called each time a form is deleted
                added: (function(row) {
                    performActions();
                    alternatingRows(row);
                }),                                // Function called each time a new form is added
            });
        }
        formset();
    });
})(jQuery);
