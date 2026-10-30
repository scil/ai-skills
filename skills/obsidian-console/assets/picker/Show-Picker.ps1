# Show-Picker: the choice window for a console button that must ask what to act on (a playbook,
# hosts, environments). Copy this file next to the project's runner and dot-source it from the
# script the key runs; that script reads the lists from the repository on every click, so new
# files and hosts appear without editing the note or data.json.
# Returns $null on Cancel, else [pscustomobject]@{ Choice = <drop-down value>; Names = <ticked names> }.
# The caller validates the result again: the window is a convenience, not the guard.
function Show-Picker {
    param(
        [Parameter(Mandatory = $true)][string]$Title,
        [Parameter(Mandatory = $true)][object[]]$Items,  # objects with Name, and Blocked ('' or the reason)
        [string]$ItemLabel = 'Targets',
        [string]$ChoiceLabel = '',                       # empty: no drop-down
        [string[]]$Choices = @(),
        [switch]$Single,                                 # at most one ticked item
        [string]$OkText = 'OK'
    )
    Add-Type -AssemblyName System.Windows.Forms
    $form = New-Object System.Windows.Forms.Form -Property @{
        Text = $Title; Width = 560; TopMost = $true; StartPosition = 'CenterScreen'
        FormBorderStyle = 'FixedDialog'; MaximizeBox = $false; MinimizeBox = $false
    }
    $y = 12
    $combo = $null
    if ($ChoiceLabel) {
        $form.Controls.Add((New-Object System.Windows.Forms.Label -Property @{ Text = $ChoiceLabel; Left = 12; Top = $y; AutoSize = $true }))
        $combo = New-Object System.Windows.Forms.ComboBox -Property @{ Left = 12; Top = $y + 22; Width = 520; DropDownStyle = 'DropDownList' }
        $Choices | ForEach-Object { [void]$combo.Items.Add($_) }
        if ($combo.Items.Count) { $combo.SelectedIndex = 0 }
        $form.Controls.Add($combo)
        $y += 64
    }
    $form.Controls.Add((New-Object System.Windows.Forms.Label -Property @{ Text = $ItemLabel; Left = 12; Top = $y; AutoSize = $true }))
    $list = New-Object System.Windows.Forms.CheckedListBox -Property @{ Left = 12; Top = $y + 22; Width = 520; Height = 200; CheckOnClick = $true }
    foreach ($i in $Items) {
        [void]$list.Items.Add($(if ($i.Blocked) { "$($i.Name)   (blocked: $($i.Blocked))" } else { $i.Name }))
    }
    # A blocked item stays visible with its reason but cannot be ticked; -Single unticks the others.
    $list.Add_ItemCheck({
            param($s, $a)
            if ($Items[$a.Index].Blocked) { $a.NewValue = 'Unchecked'; return }
            if ($Single -and $a.NewValue -eq 'Checked') {
                foreach ($k in @($s.CheckedIndices)) { if ($k -ne $a.Index) { $s.SetItemChecked($k, $false) } }
            }
        })
    $y += 240
    $ok = New-Object System.Windows.Forms.Button -Property @{ Text = $OkText; Left = 312; Top = $y; Width = 110; DialogResult = 'OK' }
    $cancel = New-Object System.Windows.Forms.Button -Property @{ Text = 'Cancel'; Left = 432; Top = $y; Width = 100; DialogResult = 'Cancel' }
    $form.Controls.AddRange(@($list, $ok, $cancel))
    $form.ClientSize = New-Object System.Drawing.Size(544, ($y + 40))
    $form.AcceptButton = $ok
    $form.CancelButton = $cancel
    $form.Add_Shown({ $form.Activate() })  # the Shell commands process has no window; bring this one forward
    if ($form.ShowDialog() -ne 'OK') { return $null }
    [pscustomobject]@{
        Choice = if ($combo) { [string]$combo.SelectedItem } else { '' }
        Names  = @(@($list.CheckedIndices) | ForEach-Object { $Items[$_].Name })
    }
}
