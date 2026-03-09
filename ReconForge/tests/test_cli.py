from reconforge.cli.main import build_parser


def test_parser_includes_commands() -> None:
    parser = build_parser()
    args = parser.parse_args(["discover", "example.com"])
    assert args.command == "discover"
    assert args.target == "example.com"
