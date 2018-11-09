function fit_to_screen()
    scale = 2562.0 / mp.get_property("width")
    mp.set_property("window-scale", scale)
end

mp.add_key_binding("alt+`", "Fit_Screen", fit_to_screen)