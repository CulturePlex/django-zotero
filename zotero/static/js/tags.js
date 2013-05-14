(function($) {
    $(document).ready(function($) {
        // GENERAL VARIABLES
        var admin_url = '/admin/';
        var prefix = 'zotero-tag-content_type-object_id';
        var numForms = 4;
        var numFields = 133;
        
        
        // SELECTORS
        // Item types
        var itemType = 'item_type';
        var itemTypeLabelAll = 'label[for^="id_' + prefix + '"][for$="' + itemType + '"]';
        var itemTypeLabelFirst = itemTypeLabelAll + ':first';
        var itemTypeSelectAll = 'select[id^="id_' + prefix + '"][id$="' + itemType + '"]'
        var itemTypeSelectFirst = itemTypeSelectAll + ':first';
        
        // Fields
        var field = 'field';
        var fieldSelectAll = 'select[id^="id_' + prefix + '"][id$="' + field + '"]'
        var fieldSelectFirst = fieldSelectAll + ':first';
        var fieldSelectLast = fieldSelectAll + ':last';
        
        // Values
        var value = 'value'
        
        // Deletes
        var del = 'DELETE';
        var deleteCheckboxAll = 'input[id^="id_' + prefix + '"][id$="' + del + '"]';
        var deleteCheckboxLast = deleteCheckboxAll + ':last';
        
        // Links
        var add = 'add_tag';
        var a = '<a href="javascript:void(0)" id="id_' + prefix + '-0-' + add + '">Add another tag</a>';
        var linkUnique = 'a[id^="id_' + prefix + '"][id$="' + add + '"]';
        
        
        // NEW ELEMENTS
        var addLink = function() {
            $(deleteCheckboxLast).after(a);
        }
        addLink();
        
        
        // STYLE
        // Add brs
        var addBrs = function() {
            var br1 = "<br/>"
            var br2 = "<br/><br/>"
            $(itemTypeLabelFirst).before(br2);
            $(itemTypeSelectFirst).after(br2);
            $(deleteCheckboxAll).after(br1);
            $(linkUnique).before(br1);
            $(linkUnique).after(br2);
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
                
                // Listen to click events from "Add another Tag"
                $(linkUnique).bind('click', addTag);
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
        
        // Add tags
        var addTag =  function() {
            var row = createNewRow();
            $(deleteCheckboxLast).after('<br/>' + row);
            $(fieldSelectLast).val(0);
            performActions();
            $("#id_" + prefix + "-TOTAL_FORMS").val(numForms + 1);

        }
        
        var createNewRow =  function() {
            var itemType = createItemType();
            var field = createField();
            var value = createValue();
            var del = createDelete();
            return itemType + field + value + del;
        }
        
        var createItemType =  function() {
            var label = '<label';
            label += ' for="id_' + prefix + '-' + numForms + '-' + itemType + '">';
            label += 'Item type:';
            label += '</label>';
            var select = '<select';
            select += ' name="' + prefix + '-' + numForms + '-' + itemType + '"';
            select += ' id="id_' + prefix + '-' + numForms + '-' + itemType + '">';
            select += $(itemTypeSelectFirst).html();
            select += '</select>';
            return label + select;
        }
        
        var createField =  function() {
            var label = '<label';
            label += ' for="id_' + prefix + '-' + numForms + '-' + field + '">';
            label += 'Field:';
            label += '</label>';
            var select = '<select';
            select += ' name="' + prefix + '-' + numForms + '-' + field + '"';
            select += ' id="id_' + prefix + '-' + numForms + '-' + field + '">';
            select += $(fieldSelectFirst).html();
            select += '</select>';
            return label + select;
        }
        
        var createValue =  function() {
            var label = '<label';
            label += ' for="id_' + prefix + '-' + numForms + '-' + value + '">';
            label += 'Value:';
            label += '</label>';
            var input = '<input'
            input += ' name="' + prefix + '-' + numForms + '-' + value + '"'
            input += ' id="id_' + prefix + '-' + numForms + '-' + value + '"'
            input += ' type="text"'
            input += ' name="' + prefix + '-' + numForms + '-' + value + '"'
            input += ' value="" maxlength="256"/>'
            return label + input;
        }
        
        var createDelete =  function() {
            var label = '<label';
            label += ' for="id_' + prefix + '-' + numForms + '-' + del + '">';
            label += 'Delete:';
            label += '</label>';
            var input = '<input'
            input += ' name="' + prefix + '-' + numForms + '-' + del + '"'
            input += ' id="id_' + prefix + '-' + numForms + '-' + del + '"'
            input += ' type="checkbox"'
            input += ' name="' + prefix + '-' + numForms + '-' + del + '"'
            input += ' value="" maxlength="256"/>'
            return label + input;
        }
        
        // Delete tags
        var deleteTag =  function() {
            
            $(LinkUnique).click(performActions);
        }
    });
})(django.jQuery);
