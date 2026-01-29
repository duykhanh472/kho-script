-- Xóa span rỗng chỉ dùng làm anchor
function Span(el)
  if #el.content == 0 then
    return {}
  end

  -- Xóa mọi thuộc tính lang
  el.attributes["lang"] = nil

  -- Xóa class
  el.classes = {}

  -- Xóa id
  el.identifier = ""

  return el
end

function Image(el)
  el.attributes = {}
  el.classes = {}
  return el
end

-- Làm sạch heading
function Header(el)
  el.attributes = {}
  el.classes = {}
  el.identifier = ""
  return el
end
