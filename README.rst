Setup::

  cp bin/* ~/bin/
  [ -d ~/.profile.d ] || mkdir ~/.profile.d
  cp profile.d/* ~/.profile.d/

  echo << EOF >> ~/.bashrc
  # ashley's aws hacks
  [ -f ~/.profile.d/aws_functions.sh ] && source ~/.profile.d/aws_functions.sh
  EOF

  . ~/.bashrc



