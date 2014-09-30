// Generated by CoffeeScript 1.7.1
(function() {
  var Dashboard, GameEngine, app, login,
    __slice = [].slice;

  Dashboard = (function() {
    function Dashboard() {}

    Dashboard.prototype.ajax = function(url, data, successFunc) {
      if (successFunc == null) {
        successFunc = function() {};
      }
      return $.ajax({
        url: url,
        dataType: "json",
        data: data,
        cache: false,
        error: function(xhr, msg) {},
        success: successFunc
      });
    };

    Dashboard.prototype.quick_match = function() {
      var begin_match, btn, find_opponent, max_request, num_requested;
      btn = $('#quick_match');
      max_request = 5;
      num_requested = 0;
      find_opponent = (function(_this) {
        return function(callback) {
          btn.html('Searching...');
          if (num_requested >= max_request) {
            console.log("Max " + max_request + " requests exceeded");
            btn.html('Quick Match');
            return;
          }
          num_requested += 1;
          return _this.ajax(_this.quick_match_url, {}, function(rval) {
            if (rval.opponent_id) {
              btn.html('Quick Match');
              return callback(rval.redirect_url);
            } else {
              return setTimeout((function() {
                return find_opponent(callback);
              }), 3000);
            }
          });
        };
      })(this);
      begin_match = function(redirect_url) {
        return window.location = redirect_url;
      };
      return find_opponent(begin_match);
    };

    return Dashboard;

  })();

  this.init_dashboard = function(quick_match_url) {
    var dashboard;
    dashboard = new Dashboard();
    dashboard.quick_match_url = quick_match_url;
    return $('#quick_match').click(function() {
      return dashboard.quick_match();
    });
  };

  GameEngine = (function() {
    GameEngine.prototype.url_board = null;

    GameEngine.prototype.url_progress = null;

    GameEngine.prototype.url_move = null;

    GameEngine.prototype.update_interval = null;

    GameEngine.prototype.renderer = null;

    GameEngine.prototype.board_id = null;

    function GameEngine(container_id, width, height, user_id) {
      this.renderer = new Engine(container_id, width, height, user_id);
    }

    GameEngine.prototype.start = function() {
      var fn, self;
      self = this;
      fn = function() {
        return (function() {
          return this.ajax(this.url_progress, this.update_interval, {}, this.drawBoard);
        }).call(self);
      };
      return setInterval(fn, this.update_interval);
    };

    GameEngine.prototype.drawBoard = function(data) {
      return this.renderer.updateBoard(data.board_users, data[this.board_id], data.moves);
    };

    GameEngine.prototype.ajax = function(url, timeout, data, successFunc) {
      if (successFunc == null) {
        successFunc = function() {};
      }
      data['board_id'] = this.board_id;
      return $.ajax({
        url: url,
        dataType: "json",
        data: data,
        cache: false,
        context: this,
        timeout: timeout,
        error: function(xhr, msg) {},
        success: successFunc
      });
    };

    return GameEngine;

  })();

  this.init_svg_game = function(playground, width, height, user_id) {
    if (typeof Engine === "undefined") {
      throw new Error("Render engine has not been included!");
      return;
    }
    return new GameEngine(playground, width, height, user_id);
  };

  app = angular.module('app', []);

  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });

  app.controller('gameController', function($scope, $interval, $element) {
    var init, reset_game_settings, run_ai, scopeWrap, socket, svg_game, svg_game_move;
    scopeWrap = function(fn) {
      return function() {
        var args;
        args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return $scope.$apply(function() {
          return fn.apply(null, args);
        });
      };
    };
    socket = io.connect($element.attr('data-url'));
    $scope.games = [];
    $scope.player_id = null;
    svg_game = null;
    reset_game_settings = function() {
      $scope.game_id = null;
      $scope.players = {};
      $scope.is_ready = false;
      $scope.is_host = false;
      return $scope.is_game_started = false;
    };
    init = function() {
      reset_game_settings();
      $scope.is_ready = true;
      $scope.is_host = true;
      $scope.join('game_' + $element.attr('data-key'));
      return $scope.$watch('is_ready', function(is_ready) {
        if (!$scope.game_id) {
          return;
        }
        socket.emit('tick_ready', $scope.game_id, is_ready);
        return $scope.players[$scope.player_id] = is_ready;
      });
    };
    $scope.host_new = function(e, v) {
      reset_game_settings();
      return socket.emit('host_game', function(new_game_id) {
        $scope.game_id = new_game_id;
        $scope.players[$scope.player_id] = $scope.is_ready;
        return $scope.is_host = true;
      });
    };
    $scope.join = function(game_id) {
      return socket.emit('join_game', game_id, $scope.is_ready, scopeWrap(function(players) {
        $scope.game_id = game_id;
        $scope.players = players;
        return $scope.players[$scope.player_id] = $scope.is_ready;
      }));
    };
    $scope.start_game = function() {
      return socket.emit('start_game', $scope.game_id, _.keys($scope.players));
    };
    $scope.is_room_ready = function() {
      if (!$scope.game_id) {
        return false;
      }
      if (!(_.size($scope.players) > 1)) {
        return false;
      }
      return _.all($scope.players);
    };
    socket.on('connect', scopeWrap(function() {
      $scope.player_id = socket.socket.sessionid;
      return init();
    }));
    socket.on('error', function(reason) {
      return console.error('Unable to connect server', reason);
    });
    socket.on('games', scopeWrap(function(games) {
      return $scope.games = games;
    }));
    socket.on('join', scopeWrap(function(player_id, is_ready) {
      $scope.players[player_id] = is_ready;
      return socket.emit('tick_ready', $scope.game_id, $scope.is_ready);
    }));
    socket.on('leave', scopeWrap(function(player_id) {
      return delete $scope.players[player_id];
    }));
    socket.on('data', scopeWrap(function() {
      var args, board_moves, board_powers, board_users, is_ready, player_id, player_idx, type, winner_id;
      type = arguments[0], args = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
      switch (type) {
        case 'ready_state':
          player_id = args[0], is_ready = args[1];
          return $scope.players[player_id] = is_ready;
        case 'start_game':
          player_idx = args[0];
          svg_game = new Engine('#game', 750, 600, player_idx);
          svg_game.move = svg_game_move;
          return $scope.is_game_started = true;
        case 'board':
          board_users = args[0], board_powers = args[1], board_moves = args[2];
          if ($scope.is_game_started) {
            svg_game.updateBoard(board_users, board_powers, board_moves);
            return run_ai(svg_game.user_id, board_users, board_powers, board_moves);
          }
          break;
        case 'end_game':
          winner_id = args[0];
          if (svg_game.users_id === winner_id) {
            console.log('Congrats! You win!');
          } else {
            console.log('You are lost! Try again?');
          }
          return setTimeout((function() {
            return window.location = '/game/dashboard/';
          }), 5000);
      }
    }));
    svg_game_move = function(fx, fy, tx, ty) {
      return socket.emit('move', $scope.game_id, fx, fy, tx, ty);
    };
    return run_ai = function(user_id, users, powers, moves) {
      var able, get_attackable, has_cell_at, x, y, _results, _x, _y;
      has_cell_at = function(x, y) {
        if (y in users) {
          return x in users[y];
        }
        return false;
      };
      get_attackable = function(x, y) {
        var attackable, mark_if_attackable, shift;
        shift = y % 2 ? 0 : 1;
        attackable = false;
        mark_if_attackable = function(_y, _x) {
          if (has_cell_at(_x, _y)) {
            if (users[_y][_x] !== user_id) {
              return attackable = [_x, _y];
            }
          }
        };
        mark_if_attackable(y - 1, x - 1 + shift);
        mark_if_attackable(y - 1, x + shift);
        mark_if_attackable(y, x + 1);
        mark_if_attackable(y + 1, x + shift);
        mark_if_attackable(y + 1, x - 1 + shift);
        mark_if_attackable(y, x - 1);
        return attackable;
      };
      _results = [];
      for (y in users) {
        _results.push((function() {
          var _results1;
          _results1 = [];
          for (x in users[y]) {
            if (users[y][x] !== user_id) {
              continue;
            }
            y = parseInt(y);
            x = parseInt(x);
            able = get_attackable(x, y);
            if (!able) {
              continue;
            }
            _x = able[0], _y = able[1];
            _results1.push(svg_game_move(x, y, _x, _y));
          }
          return _results1;
        })());
      }
      return _results;
    };
  });

  login = function() {
    return $.get('/game/auto_login', function(rval) {
      if (!rval) {
        return;
      }
      $('#id_phone_number').val(rval.phone_number);
      $('#id_pin_code').val(rval.pin_code);
      return $('#login-form').submit();
    });
  };

  $(function() {
    if (location.pathname === '/security/login') {
      login();
    }
    if (location.pathname === '/game/dashboard/') {
      return setTimeout((function() {
        return $('#quick_match').click();
      }), 500);
    }
  });

}).call(this);
