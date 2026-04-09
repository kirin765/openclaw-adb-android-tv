from app.services.rule_engine import RuleEngine


def test_rule_engine_matches_youtube():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("유튜브 열어줘")
    assert intent is not None
    assert intent.intent == "TV_LAUNCH_APP"
    assert intent.parameters["app"] == "youtube"


def test_rule_engine_matches_browser():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("브라우저 열어줘")
    assert intent is not None
    assert intent.intent == "OPEN_BROWSER"
    assert intent.target_device == "pc"


def test_rule_engine_matches_url():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("https://example.com")
    assert intent is not None
    assert intent.intent == "OPEN_URL"
    assert intent.parameters["url"] == "https://example.com"


def test_rule_engine_matches_remote_confirm():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("확인")
    assert intent is not None
    assert intent.intent == "TV_KEYEVENT"
    assert intent.parameters["keycode"] == 23


def test_rule_engine_matches_power_off():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("전원 꺼")
    assert intent is not None
    assert intent.intent == "TV_POWER_OFF"


def test_rule_engine_matches_power_on():
    engine = RuleEngine("config/rules.yaml")
    intent = engine.match("화면 켜기")
    assert intent is not None
    assert intent.intent == "TV_POWER_ON"
