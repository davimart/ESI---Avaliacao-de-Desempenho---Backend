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
    pip install -r requirements.txt

    # Generate a new SECRET_KEY and save it to .env
    python -c "
    import os
    from django.core.management.utils import get_random_secret_key

    env_file = '.env'
    secret_key = get_random_secret_key()

    if not os.path.exists(env_file):
        print(f'Creating {env_file} with SECRET_KEY.')
        with open(env_file, 'w') as f:
            f.write(f'SECRET_KEY={secret_key}\n')
    else:
        print(f'{env_file} already exists, not overwriting.')
    "
    echo "Development environment is ready."
  '';
}
