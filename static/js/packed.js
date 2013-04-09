// Generated by CoffeeScript 1.4.0
(function() {
  var HexController,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  HexController = (function() {

    HexController.prototype.url_board = null;

    HexController.prototype.url_progress = null;

    HexController.prototype.url_move = null;

    HexController.prototype.update_interval = null;

    HexController.prototype.hexagon_radius = null;

    HexController.prototype.update = true;

    HexController.prototype.user_id = null;

    HexController.prototype.point_start = null;

    HexController.prototype.point_end = null;

    HexController.prototype.is_ready = false;

    HexController.prototype.colors = {
      background: createjs.Graphics.getRGB(32, 38, 35),
      hex_border: createjs.Graphics.getRGB(63, 159, 112),
      hex_fill: createjs.Graphics.getRGB(6, 59, 33)
    };

    function HexController(container_id) {
      var arr, i, n, x, y, _i, _j, _n, _x, _y;
      this.container_id = container_id;
      this.time_left_to_update = 0;
      this.arrows = {};
      this.bin_array = [];
      n = 26;
      _n = 22;
      i = 0;
      y = 0;
      arr = [];
      for (_y = _i = 0; 0 <= n ? _i <= n : _i >= n; _y = 0 <= n ? ++_i : --_i) {
        x = 0;
        if (_y > 15) {
          _n -= 2;
        }
        for (_x = _j = 0; 0 <= _n ? _j <= _n : _j >= _n; _x = 0 <= _n ? ++_j : --_j) {
          this.bin_array[i++] = [x, y];
          if (_x % 2) {
            x = (_x - 1) / 2 + 1;
          } else {
            x = -_x / 2 - 1;
          }
        }
        if (_y % 2) {
          y = (_y - 1) / 2 + 1;
        } else {
          y = -_y / 2 - 1;
        }
      }
    }

    HexController.prototype.drawBackground = function() {
      var shape;
      shape = new createjs.Shape();
      shape.graphics.beginFill(this.colors.background);
      shape.graphics.rect(0, 0, this.width, this.height);
      return this.stage.addChild(shape);
    };

    HexController.prototype.show_arrow = function(point_start, point_end) {
      if (Math.abs(point_end.x - point_start.x) > this.hexagon_width + 1) {
        return;
      }
      if (Math.abs(point_end.y - point_start.y) > this.hexagon_width + 1) {
        return;
      }
      this.temp_arrow.x = point_start.x;
      this.temp_arrow.y = point_start.y;
      this.temp_arrow.rotation = this.angle_from_points(point_start, point_end);
      return this.temp_arrow;
    };

    HexController.prototype.new_hexagon = function(x, y, coord) {
      var hexagon, number_of_nodes, self;
      number_of_nodes = Math.random() * 1000000;
      hexagon = new createjs.Shape();
      hexagon.x = x;
      hexagon.y = y;
      hexagon.coord = coord;
      self = this;
      hexagon.onMouseOver = function(e) {
        if (self.point_start) {
          self.point_end = e.target;
          self.temp_arrow.visible = true;
          return self.update = true;
        }
      };
      hexagon.onPress = function(e) {
        self.point_start = e.target;
        return e.onMouseUp = function(ev) {
          if (!self.point_end) {
            self.point_end = ev.target;
          }
          if (ev.target.user_id === self.user_id) {
            self.move(self.point_start.coord, self.point_end.coord);
          }
          self.point_start = null;
          self.point_end = null;
          return self.update = true;
        };
      };
      hexagon.update = function(n, user_id, color) {
        return self.update_hexagon(hexagon, n, user_id, color);
      };
      return hexagon;
    };

    HexController.prototype.update_hexagon = function(hexagon, n, user_id, color) {
      var c, draw_bin_at, g, i, radius, x, y, _i, _ref, _ref1;
      if (hexagon.old_n === n && (hexagon.user_id = user_id)) {
        return;
      }
      g = hexagon.graphics;
      g.clear();
      hexagon.user_id = user_id;
      hexagon.old_n = n;
      color = {
        r: parseInt(color.substr(1, 2), 16),
        g: parseInt(color.substr(3, 2), 16),
        b: parseInt(color.substr(5, 2), 16)
      };
      c = createjs.Graphics.getRGB(color.r, color.g, color.b, .3);
      g.beginFill(c);
      radius = this.hexagon_radius - this.hexagon_radius * 0.1 / 2;
      g.drawPolyStar(0, 0, radius, 6, 0, -90);
      draw_bin_at = function(x, y, size, spacing) {
        var _offset;
        if (size == null) {
          size = 5;
        }
        if (spacing == null) {
          spacing = 2;
        }
        _offset = spacing + size;
        g.moveTo(x * _offset - 0.5, y * _offset - 0.5);
        g.lineTo(x * _offset + 0.5, y * _offset + 0.5);
        g.moveTo(x * _offset + 0.5, y * _offset + 0.5);
        g.lineTo(x * _offset + 1.5, y * _offset + 1.5);
        g.moveTo(x * _offset - 0.5, y * _offset + 0.5);
        g.lineTo(x * _offset + 0.5, y * _offset + 1.5);
        g.moveTo(x * _offset + 0.5, y * _offset - 0.5);
        return g.lineTo(x * _offset + 1.5, y * _offset + 0.5);
      };
      g.setStrokeStyle(1);
      c = createjs.Graphics.getRGB(color.r, color.g, color.b, 0.8);
      g.beginStroke(c);
      for (i = _i = 0, _ref = n - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        if (!(i in this.bin_array)) {
          continue;
        }
        _ref1 = this.bin_array[i], x = _ref1[0], y = _ref1[1];
        draw_bin_at(x, y, 1, 1);
      }
      if (n >= 489) {
        g.beginStroke(null);
        g.beginFill('#FFFFFF');
        g.drawPolyStar(0, -4, radius / 5, 5, 0.48, -90);
        g.drawPolyStar(5, 3, radius / 5, 5, 0.48, -90);
        g.drawPolyStar(-5, 3, radius / 5, 5, 0.48, -90);
        g.beginFill('#000000');
        g.drawPolyStar(0, -4, radius / 5, 5, 0.9, -90);
        g.drawPolyStar(5, 3, radius / 5, 5, 0.9, -90);
        g.drawPolyStar(-5, 3, radius / 5, 5, 0.9, -90);
      } else if (n >= 200) {
        g.beginStroke(null);
        g.beginFill('#FFFFFF');
        g.drawPolyStar(0, -4, radius / 5, 5, 0.48, -90);
        g.beginFill('#000000');
        g.drawPolyStar(0, -4, radius / 5, 5, 0.9, -90);
      }
      return hexagon.cache(-radius, -radius, 2 * radius, 2 * radius);
      /*
          # draw toothed progress shape
          hexagon.graphics.setStrokeStyle(1, "round")
          level = Math.floor(Math.log(n) / Math.LN10) + 1
          total_teeth = level * 10
      
          inner_radius = @hexagon_radius / 10 * level
          outer_radius = @hexagon_radius / 10 * (level + 1)
          for i in [0..(level-1)]
            if i
              hexagon.graphics.drawCircle(0, 0, @hexagon_radius / 10 * i)
      */

      /*
          # prepare random array
          num_teeth = n / Math.pow(10, level - 1) * level
      
          from = 0
          to = 0
          size = 1 / (total_teeth / 2) * Math.PI
          for i in [0..total_teeth]
            radius = if i <= num_teeth then outer_radius else inner_radius
            hexagon.graphics.arc(0, 0, radius, from, from + size, 0)
            from += size
      */

      /*
          size = Math.PI * 2 * n / Math.pow(10, level)
          hexagon.graphics.arc(0, 0, inner_radius, 0, size, 0)
      */

    };

    HexController.prototype.move = function(from, to) {
      var params;
      params = {
        fx: from.x,
        fy: from.y,
        tx: to.x,
        ty: to.y
      };
      return this.ajax(this.url_move, 3000, params);
    };

    HexController.prototype.dotted_arrow = function(x, y, rotation) {
      var arrow, g, i, self, size;
      if (rotation == null) {
        rotation = 0;
      }
      arrow = new createjs.Shape();
      g = arrow.graphics;
      arrow.color = createjs.Graphics.getRGB(255, 255, 255, .1);
      size = this.hexagon_radius * 2 - 5.5;
      self = this;
      arrow.update = function() {
        var i, n, _results;
        g.clear();
        g.setStrokeStyle(1);
        g.beginStroke(arrow.color);
        _results = [];
        for (i in arrow.dots) {
          n = arrow.dots[i] + 2;
          if (n > size) {
            n = 0;
          }
          g.rect(0, -n, 1, 1);
          _results.push(arrow.dots[i] = n);
        }
        return _results;
      };
      arrow.dots = (function() {
        var _i, _results;
        _results = [];
        for (i = _i = 0; _i <= 3; i = ++_i) {
          _results.push(i * 8);
        }
        return _results;
      })();
      arrow.rotation = rotation;
      arrow.x = x;
      arrow.y = y;
      arrow.update();
      return arrow;
    };

    HexController.prototype.drag_arrow = function(x, y, rotation) {
      var arrow, coef, g, i, offset_x, offset_y, scaled_size, size, _i;
      if (rotation == null) {
        rotation = 0;
      }
      arrow = new createjs.Shape();
      g = arrow.graphics;
      size = this.hexagon_radius / 1.5;
      arrow.regX = size;
      arrow.regY = size * 2;
      coef = 0.75;
      scaled_size = size;
      for (i = _i = 1; _i <= 5; i = ++_i) {
        offset_x = size - scaled_size / 2;
        offset_y = offset_x * 3 - size;
        arrow.graphics.moveTo(offset_x, offset_y);
        arrow.graphics.setStrokeStyle(scaled_size / 7);
        arrow.graphics.beginStroke("#FFFFFF");
        arrow.graphics.lineTo(offset_x + scaled_size / 2, offset_y - scaled_size / 2);
        arrow.graphics.lineTo(offset_x + scaled_size, offset_y);
        arrow.graphics.endStroke();
        scaled_size = scaled_size * coef;
      }
      arrow.rotation = rotation;
      arrow.x = x;
      arrow.y = y;
      return arrow;
    };

    HexController.prototype.init_board = function(self, json) {
      /*
          A callback function for board details
          Initialize board by drawing into stage
      */

      var board, cell, cell_rows, offset_x, offset_y, pos_x, pos_y, shape, x, y;
      board = json[json.board_id];
      self.cells = [];
      offset_x = 100;
      offset_y = 100;
      for (y in board) {
        cell_rows = new Array();
        for (x in board[y]) {
          if (!board[y][x]) {
            continue;
          }
          pos_x = self.hexagon_width * x - (y % 2) * self.hexagon_width / 2;
          pos_y = self.hexagon_radius * 1.5 * y;
          shape = self.new_hexagon(offset_x + pos_x, offset_y + pos_y, {
            x: x,
            y: y
          });
          cell = {
            arrow: null,
            hexagon: shape
          };
          self.stage.addChildAt(shape, 1);
          cell_rows[x] = cell;
        }
        self.cells.push(cell_rows);
      }
      this.is_ready = true;
    };

    HexController.prototype.draw_updated_data = function(self, data) {
      var board_data, cell_from, cell_to, cells, color, from, fx, fy, moves, rotation, to, tx, ty, user_id, visible_arrows, x, y, _i, _len, _ref, _ref1, _ref2;
      self.is_ready = false;
      self.users = data.board_users;
      cells = self.cells;
      moves = data.moves;
      board_data = data[data.board_id];
      for (y in board_data) {
        for (x in board_data[y]) {
          if (board_data[y][x]) {
            _ref = self.users[y][x], user_id = _ref[0], color = _ref[1];
            cells[y][x].hexagon.update(board_data[y][x], user_id, color);
          }
        }
      }
      visible_arrows = [];
      for (_i = 0, _len = moves.length; _i < _len; _i++) {
        _ref1 = moves[_i], fy = _ref1[0], fx = _ref1[1], tx = _ref1[2], ty = _ref1[3];
        cell_from = cells[fx][fy];
        cell_to = cells[ty][tx];
        from = {
          x: cell_from.hexagon.x,
          y: cell_from.hexagon.y
        };
        to = {
          x: cell_to.hexagon.x,
          y: cell_to.hexagon.y
        };
        rotation = self.angle_from_points(from, to);
        if (cell_from.arrow) {
          cell_from.arrow.rotation = rotation;
        } else {
          cell_from.arrow = self.dotted_arrow(from.x, from.y, rotation);
          self.stage.addChildAt(cell_from.arrow, 1);
        }
        visible_arrows.push(fy + '_' + fx);
      }
      for (y in cells) {
        for (x in cells[y]) {
          if (cells[y][x].arrow) {
            cells[y][x].arrow.visible = (_ref2 = x + '_' + y, __indexOf.call(visible_arrows, _ref2) >= 0);
          }
        }
      }
      self.is_ready = true;
      self.update = true;
    };

    HexController.prototype.start = function() {
      var $canvas, $container;
      this.hexagon_width = this.hexagon_radius * Math.sqrt(3);
      $canvas = $('<canvas></canvas>');
      $container = $(this.container_id).append($canvas);
      this.set_nondraggable($container);
      this.width = $container.width();
      this.height = $container.height();
      $canvas.attr({
        width: this.width,
        height: this.height
      });
      this.stage = new createjs.Stage($canvas.get(0));
      this.stage.enableMouseOver();
      this.ajax(this.url_board, 2000, {
        board_id: 'board1'
      }, this.init_board);
      this.drawBackground();
      this.fpsLabel = new createjs.Text("-- fps", "bold 18px Arial", "#777");
      this.stage.addChild(this.fpsLabel);
      this.fpsLabel.x = 10;
      this.fpsLabel.y = 20;
      this.temp_arrow = this.drag_arrow(0, 0, null);
      this.stage.addChild(this.temp_arrow);
      this.stage.update();
      createjs.Ticker.addListener(this);
      return createjs.Ticker.setFPS(50);
    };

    HexController.prototype.tick = function(time_passed) {
      var x, y;
      if (this.update) {
        if (this.point_start && this.point_end && (this.point_start.user_id === this.user_id)) {
          if (this.point_start.x !== this.point_end.x || this.point_start.y !== this.point_end.y) {
            this.show_arrow(this.point_start, this.point_end);
          }
        } else {
          this.temp_arrow.visible = false;
        }
        this.fpsLabel.text = Math.round(createjs.Ticker.getMeasuredFPS()) + " fps";
        this.update = false;
        this.stage.update();
      }
      if (!this.arrow_speed || this.arrow_speed < 0) {
        this.arrow_speed = 200;
        for (y in this.cells) {
          for (x in this.cells[y]) {
            if (this.cells[y][x].arrow) {
              this.cells[y][x].arrow.update();
            }
          }
        }
        this.update = true;
      }
      this.arrow_speed -= time_passed;
      this.time_left_to_update -= time_passed;
      if (this.time_left_to_update <= 0) {
        this.time_left_to_update += this.update_interval;
        return this.ajax(this.url_progress, this.update_interval, {}, this.draw_updated_data);
      }
    };

    HexController.prototype.set_nondraggable = function(element) {
      return $(element).on('dragstart', function(e) {
        e.preventDefault();
      });
    };

    HexController.prototype.angle_from_points = function(point_start, point_end) {
      var a, angle, b, c;
      b = point_end.y - point_start.y;
      c = point_end.x - point_start.x;
      a = Math.sqrt(b * b + c * c);
      angle = Math.acos(b / a) * 180 / Math.PI;
      if (c > 0) {
        angle = 360 - angle;
      }
      angle += 180;
      return angle;
    };

    HexController.prototype.ajax = function(url, timeout, data, successFunc) {
      var self;
      if (successFunc == null) {
        successFunc = function() {};
      }
      data['board_id'] = this.board_id;
      self = this;
      return $.ajax({
        url: url,
        dataType: "json",
        data: data,
        cache: false,
        timeout: timeout,
        error: function(xhr, msg) {},
        success: function(json) {
          return successFunc(self, json);
        }
      });
    };

    return HexController;

  })();

  this.init_game = function(playground) {
    return new HexController(playground);
  };

  $(function() {});

}).call(this);
