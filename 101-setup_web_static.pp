# File: 101-setup_web_static.pp

package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'root',
  group  => 'root',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>',
  owner   => 'root',
  group   => 'root',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'root',
  group  => 'root',
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
  notify  => Exec['nginx-reload'],
}

exec { 'nginx-reload':
  command     => 'nginx -s reload',
  refreshonly => true,
  subscribe   => File['/data/web_static/current'],
}
