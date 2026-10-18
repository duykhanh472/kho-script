-- ==============================================================================
-- Subtitle Hider cho MPV
-- Chức năng: Tạo một dải băng đen che hardsub để thực hành "raw listening"
-- ==============================================================================

local mp = require 'mp'
local msg = require 'mp.msg'
local options = require 'mp.options'

-- 1. Cấu hình mặc định
local opts = {
    enabled = false,
    margin_bottom = 0,
    box_height = 12,
    box_width = 100,
    step = 1
}

-- Đọc file cấu hình từ ~/.config/mpv/script-opts/subtitle_hider.conf
options.read_options(opts, "subtitle_hider")

-- Đường dẫn lưu tệp cấu hình (~~/ trỏ vào thư mục config của MPV)
local config_path = mp.command_native({"expand-path", "~~/script-opts/subtitle_hider.conf"})

-- Hàm ghi lại các thông số hiện tại vào tệp cấu hình
local function save_settings()
    local file = io.open(config_path, "w")
    if file then
        file:write(string.format("enabled=%s\n", opts.enabled and "yes" or "no"))
        file:write(string.format("margin_bottom=%d\n", opts.margin_bottom))
        file:write(string.format("box_height=%d\n", opts.box_height))
        file:write(string.format("box_width=%d\n", opts.box_width))
        file:write(string.format("step=%d\n", opts.step))
        file:close()
    end
end

-- Trạng thái
local is_visible = opts.enabled
local overlay = mp.create_osd_overlay("ass-events")

-- 2. Hàm vẽ hộp đen (Sử dụng ASS format)
local function draw_overlay()
    if not is_visible then
        overlay:remove()
        return
    end

    -- Đặt hệ tọa độ nội bộ của overlay về mức 100x100
    overlay.res_x = 100
    overlay.res_y = 100

    -- Tính toán toạ độ (Căn giữa theo chiều ngang)
    local x1 = (100 - opts.box_width) / 2
    local x2 = x1 + opts.box_width
    local y2 = 100 - opts.margin_bottom
    local y1 = y2 - opts.box_height

    -- Vẽ hình chữ nhật đen đặc (\1a&H00& = Opaque 100%)
    local draw_cmd = string.format(
        "{\\pos(0,0)}{\\an7}{\\bord0}{\\1a&H00&}{\\1c&H000000&}{\\p1}m %f %f l %f %f l %f %f l %f %f{\\p0}",
        x1, y1, x2, y1, x2, y2, x1, y2
    )

    overlay.data = draw_cmd
    overlay:update()
end

-- 3. Các hàm điều khiển
local function toggle_hider()
    is_visible = not is_visible
    opts.enabled = is_visible
    draw_overlay()
    save_settings()
    mp.osd_message("Subtitle Hider: " .. (is_visible and "ON" or "OFF"), 2)
end

local function move_up()
    opts.margin_bottom = math.min(100 - opts.box_height, opts.margin_bottom + opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Pos: %d%% từ dưới lên", opts.margin_bottom), 1)
end

local function move_down()
    opts.margin_bottom = math.max(0, opts.margin_bottom - opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Pos: %d%% từ dưới lên", opts.margin_bottom), 1)
end

local function increase_height()
    opts.box_height = math.min(100, opts.box_height + opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Height: %d%%", opts.box_height), 1)
end

local function decrease_height()
    opts.box_height = math.max(1, opts.box_height - opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Height: %d%%", opts.box_height), 1)
end

local function increase_width()
    opts.box_width = math.min(100, opts.box_width + opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Width: %d%%", opts.box_width), 1)
end

local function decrease_width()
    opts.box_width = math.max(1, opts.box_width - opts.step)
    draw_overlay()
    save_settings()
    mp.osd_message(string.format("Hider Width: %d%%", opts.box_width), 1)
end

-- Tính năng Peek: Nhấn giữ để xem phụ đề, nhả ra để tiếp tục che
local function peek_hider(table)
    if not is_visible then return end
    
    if table.event == "down" then
        overlay:remove()
    elseif table.event == "up" then
        draw_overlay()
    end
end

-- Khởi tạo lần đầu
draw_overlay()

-- 4. Gán phím tắt (Keybindings)
mp.add_key_binding("Ctrl+Shift+h", "toggle_hider", toggle_hider)
mp.add_key_binding("Ctrl+UP", "hider_move_up", move_up)
mp.add_key_binding("Ctrl+DOWN", "hider_move_down", move_down)
mp.add_key_binding("Alt+UP", "hider_inc_height", increase_height)
mp.add_key_binding("Alt+DOWN", "hider_dec_height", decrease_height)
mp.add_key_binding("Alt+LEFT", "hider_dec_width", decrease_width)
mp.add_key_binding("Alt+RIGHT", "hider_inc_width", increase_width)

-- Đăng ký phím Peek
mp.add_key_binding("g", "hider_peek", peek_hider, {complex = true})
