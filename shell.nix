{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.django
    pkgs.python312Packages.djangorestframework
    pkgs.python312Packages.requests
    pkgs.python312Packages.python-dotenv
    pkgs.python312Packages.faker
    pkgs.python312Packages.drf-yasg
  ];

  shellHook = ''
    python -m venv venv
    source venv/bin/activate
    pip install -U pip setuptools wheel
    pip install django djangorestframework requests python-dotenv faker drf-yasg
    
  '';
}
