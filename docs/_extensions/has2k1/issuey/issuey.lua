
--- stringify
--
-- pandoc.utils.stringify craches on nil values,
-- this version uses pcall to prevent prevent typos or
-- unspecified options from crashing the extension
--- @param el any pandoc element to be stringified
--- @return string
local function _stringify(el)
  local status, value = pcall(pandoc.utils.stringify, el)
  if status then return value else return "" end
end

return {
  ["issue"] = function(args, _, meta)
    local id = args[1]
    local url = _stringify(meta["issuey.issue-url"])
    local text = _stringify(meta["issuey.issue-text"])
    local title = _stringify(meta["issuey.issue-title"])
    url = string.gsub(url, "%%id", id)
    text = string.gsub(text, "%%id", id)
    title = string.gsub(title, "%%id", id)
    return pandoc.Link(text, url, title)
  end,

  ["pr"] = function(args, _, meta)
    local id = args[1]
    local url = _stringify(meta["issuey.pull-request-url"])
    local text = _stringify(meta["issuey.pull-request-text"])
    local title = _stringify(meta["issuey.pull-request-title"])
    url = string.gsub(url, "%%id", id)
    text = string.gsub(text, "%%id", id)
    title = string.gsub(title, "%%id", id)
    return pandoc.Link(text, url, title)
  end

}
