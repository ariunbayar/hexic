// Generated by CoffeeScript 1.4.0
(function() {
  var HexController, hexEnv, moveURL, movethem, progressInterval, retrieveBoardURL, retrieveProgressURL;

  hexEnv = {};

  hexEnv.mouse_down = false;

  hexEnv.from = {
    x: -1
  };

  hexEnv.cellHeight = 43;

  hexEnv.cellWidth = 50;

  hexEnv.moveFunc = function(from, to) {};

  hexEnv.cells = [];

  hexEnv.arrows = {};

  hexEnv.posEqual = function(a, b) {
    return (a.x === b.x) && (a.y === b.y);
  };

  hexEnv.mouseDown = function(e) {
    if (!this.board.data("is_ready")) {
      return;
    }
    if (this.mouse_down) {
      return;
    }
    this.mouse_down = true;
    this.from = $.extend(true, {}, $(e.currentTarget).data("position"));
  };

  hexEnv.posEqual = function(a, b) {
    return (a.x === b.x) && (a.y === b.y);
  };

  hexEnv.mouseUp = function(e) {
    var to;
    if (!this.board.data("is_ready")) {
      return;
    }
    this.mouse_down = false;
    to = $(e.currentTarget).data("position");
    if (this.from.x === -1 || to.x === -1) {
      return;
    }
    if (this.posEqual(this.from, to)) {
      if (!((to.x + "_" + to.y) in this.arrows)) {
        return;
      }
    }
    if ("temp" in this.arrows) {
      this.arrows["temp"].hide();
    }
    this.moveFunc(this.from, to, this.board.attr("id"));
  };

  hexEnv.cellLeave = function() {
    if (!this.board.data("is_ready")) {
      return;
    }
    if (!this.mouse_down) {
      return this.from.x = -1;
    }
  };

  hexEnv.showArrow = function(e) {
    var tmparr, to;
    if (!this.board.data("is_ready")) {
      return;
    }
    if (this.from.x === -1) {
      return;
    }
    to = $(e.currentTarget).data("position");
    if (this.posEqual(this.from, to)) {
      if ("temp" in this.arrows) {
        return this.arrows["temp"].hide();
      }
    } else {
      tmparr = this.drawArrow(this.from, to, "temp");
      return tmparr.data("pos", this.from.x + "_" + this.from.y);
    }
  };

  hexEnv.drawArrow = function(from, to, key) {
    var $arrow, arrow, pos;
    arrow = this.vector2arrow(from, to);
    if (arrow.length === 0) {
      return;
    }
    key = (typeof key === "undefined" ? from.x + "_" + from.y : key);
    if (key in this.arrows) {
      $arrow = this.arrows[key];
      $arrow.attr("class", "arrow " + arrow).show();
    } else {
      $arrow = this.newArrow(arrow);
      this.arrows[key] = $arrow;
      this.board.append($arrow);
    }
    pos = this.cells[from.x][from.y].position();
    $arrow.css({
      top: (pos.top - 20) + "px",
      left: (pos.left - 20) + "px"
    });
    return $arrow;
  };

  hexEnv.newArrow = function(arrow) {
    var attrs;
    attrs = {
      "class": "arrow " + arrow
    };
    return $("<div></div>").attr(attrs);
  };

  hexEnv.vector2arrow = function(from, to) {
    var arrow, xx;
    arrow = "";
    xx = from.x;
    if (from.y % 2 === 0) {
      xx += 1;
    }
    if ((to.x - 1 === from.x) && (to.y === from.y)) {
      arrow = "arrow-0";
    }
    if ((to.x === xx) && (to.y - 1 === from.y)) {
      arrow = "arrow-60";
    }
    if ((to.x + 1 === xx) && (to.y - 1 === from.y)) {
      arrow = "arrow-120";
    }
    if ((to.x + 1 === from.x) && (to.y === from.y)) {
      arrow = "arrow-180";
    }
    if ((to.x + 1 === xx) && (to.y + 1 === from.y)) {
      arrow = "arrow-240";
    }
    if ((to.x === xx) && (to.y + 1 === from.y)) {
      arrow = "arrow-300";
    }
    return arrow;
  };

  hexEnv.bindEventsTo = function(board) {
    board.find(".cell").bind("mouseenter", $.proxy(this, "showArrow"));
    board.find(".cell").bind("mouseleave", $.proxy(this, "cellLeave"));
    board.find(".cell").bind("mousedown", $.proxy(this, "mouseDown"));
    return board.find(".cell").bind("mouseup", $.proxy(this, "mouseUp"));
  };

  hexEnv.initBoard = function(user_id, board_id, board_data, board_users, moveFunc) {
    var board, cell, cellback, cells, x, y;
    cells = [];
    board = $("#" + board_id);
    y = 0;
    while (y < board_data.length) {
      x = 0;
      while (x < board_data[y].length) {
        if (typeof cells[x] === "undefined") {
          cells[x] = [];
        }
        cells[x][y] = 0;
        x++;
      }
      y++;
    }
    y = 0;
    while (y < board_data.length) {
      x = 0;
      while (x < board_data[y].length) {
        if (board_data[y][x] <= 0) {
          continue;
        }
        cellback = $("<div class=\"cell-back\"></div>");
        cell = $("<div class=\"cell\"></div>");
        cellback.css({
          top: (y * this.cellHeight) + "px",
          left: (x * this.cellWidth + (y % 2 ? 0 : this.cellWidth / 2)) + "px"
        });
        cell.css({
          top: (y * this.cellHeight + 7) + "px",
          left: (x * this.cellWidth + (y % 2 ? 0 : this.cellWidth / 2)) + "px"
        });
        board.append(cellback);
        board.append(cell);
        cell.data("position", {
          x: x,
          y: y
        });
        cell.data("back", cellback);
        cells[x][y] = cell;
        x++;
      }
      y++;
    }
    this.user_id = user_id;
    this.cells = cells;
    this.bindEventsTo(board);
    this.board = board;
    this.users = board_users;
    return this.moveFunc = moveFunc;
  };

  hexEnv.ajax = function(url, timeout, data, successFunc) {
    return $.ajax({
      url: url,
      dataType: "json",
      data: data,
      cache: false,
      timeout: timeout,
      success: successFunc,
      error: function(xhr, msg) {}
    });
  };

  hexEnv.drawBoard = function(moves, board_data, board_users) {
    var arr, arrows, background, cells, i, key, mentions, move, n, tmparr, x, y;
    this.board.data("is_ready", false);
    this.users = board_users;
    cells = this.cells;
    y = 0;
    while (y < board_data.length) {
      x = 0;
      while (x < board_data[y].length) {
        if (board_data[y][x]) {
          n = board_data[y][x];
          if (n >= 9000) {
            n = Math.round(n / 1000) + "k";
          } else {
            if (n >= 100) {
              n = Math.round(n / 100) / 10 + "k";
            }
          }
          cells[x][y].html(n);
          if (this.users[y][x][0] === this.user_id) {
            cells[x][y].attr("class", "cell cellfriend");
          } else {
            cells[x][y].attr("class", "cell cellfoe");
          }
          background = cells[x][y].data("back");
          background.attr("class", "cell-back cell" + board_users[y][x][1]);
        }
        x++;
      }
      y++;
    }
    mentions = [];
    tmparr = [];
    if ("temp" in this.arrows) {
      tmparr = this.arrows["temp"];
      mentions[0] = tmparr;
    }
    i = 0;
    while (i < moves.length) {
      move = moves[i];
      arr = this.drawArrow({
        x: move[0],
        y: move[1]
      }, {
        x: move[2],
        y: move[3]
      });
      key = move[0] + "_" + move[1];
      if (tmparr.lenght) {
        if (tmparr.data('pos') === key) {
          tmparr.hide();
        }
      }
      mentions[mentions.length] = key;
      i++;
    }
    arrows = this.arrows;
    $.each(arrows, function(k, arr) {
      if (mentions.indexOf(k) === -1) {
        arr.remove();
        delete arrows[k];
      }
    });
    return this.board.data("is_ready", true);
  };

  HexController = (function() {

    HexController.prototype.url_board = null;

    HexController.prototype.url_progress = null;

    HexController.prototype.url_move = null;

    HexController.prototype.update_interval = null;

    HexController.prototype.hexagon_radius = null;

    HexController.prototype.update = true;

    HexController.prototype.point_start = null;

    HexController.prototype.point_end = null;

    HexController.prototype.is_ready = false;

    HexController.prototype.colors = {
      background: createjs.Graphics.getRGB(32, 38, 35),
      hex_border: createjs.Graphics.getRGB(63, 159, 112),
      hex_fill: createjs.Graphics.getRGB(6, 59, 33)
    };

    function HexController(container_id) {
      this.container_id = container_id;
      this.time_left_to_update = 0;
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
      var hexagon, self;
      hexagon = new createjs.Shape();
      hexagon.graphics.setStrokeStyle(10, "round");
      hexagon.graphics.beginStroke(this.colors.hex_border);
      hexagon.graphics.beginFill(this.colors.hex_fill);
      hexagon.graphics.drawPolyStar(0, 0, this.hexagon_radius, 6, 0, -90);
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
          self.move(self.point_start.coord, self.point_end.coord);
          self.point_start = null;
          self.point_end = null;
          return self.update = true;
        };
      };
      hexagon.update = function(n, user_id) {
        return self.update_hexagon(hexagon, n, user_id);
      };
      return hexagon;
    };

    HexController.prototype.update_hexagon = function(hexagon, n, user_id) {
      return console.log('please implement');
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

    HexController.prototype.new_arrow = function(x, y, rotation) {
      var arrow, coef, i, num_arrows, offset_x, offset_y, scaled_size, size, _i;
      arrow = new createjs.Shape();
      size = 40;
      arrow.regX = size;
      arrow.regY = size * 2;
      num_arrows = "";
      coef = 0.75;
      scaled_size = size;
      for (i = _i = 1; _i <= 5; i = ++_i) {
        offset_x = size - scaled_size / 2;
        offset_y = offset_x * 3 - size;
        arrow.graphics.moveTo(offset_x, offset_y);
        arrow.graphics.setStrokeStyle(scaled_size / 7);
        arrow.graphics.beginStroke("#AAAAAA");
        arrow.graphics.lineTo(offset_x + scaled_size / 2, offset_y - scaled_size / 2);
        arrow.graphics.lineTo(offset_x + scaled_size, offset_y);
        arrow.graphics.endStroke();
        scaled_size = scaled_size * coef;
      }
      arrow.rotation = (rotation ? rotation : 0);
      arrow.x = x;
      arrow.y = y;
      return arrow;
    };

    HexController.prototype.init_board = function(self, json) {
      /*
          A callback function for board details
          Initialize board by drawing into stage
      */

      var board, cell, cell_rows, offset_x, offset_y, pos_x, pos_y, shape, user_id, x, y;
      user_id = $("#user_id").val();
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
      var arr, arrows, board_data, cells, i, key, mentions, move, tmparr, x, y;
      self.is_ready = false;
      self.users = data.board_users;
      cells = self.cells;
      board_data = data[data.board_id];
      for (y in board_data) {
        for (x in board_data[y]) {
          if (board_data[y][x]) {
            cells[y][x].hexagon.update(board_data[y][x], self.users[y][x][0]);
          }
        }
      }
      return;
      mentions = [];
      tmparr = [];
      if ("temp" in this.arrows) {
        tmparr = this.arrows["temp"];
        mentions[0] = tmparr;
      }
      i = 0;
      while (i < moves.length) {
        move = moves[i];
        arr = this.drawArrow({
          x: move[0],
          y: move[1]
        }, {
          x: move[2],
          y: move[3]
        });
        key = move[0] + "_" + move[1];
        if (tmparr.lenght) {
          if (tmparr.data('pos') === key) {
            tmparr.hide();
          }
        }
        mentions[mentions.length] = key;
        i++;
      }
      arrows = this.arrows;
      $.each(arrows, function(k, arr) {
        if (mentions.indexOf(k) === -1) {
          arr.remove();
          delete arrows[k];
        }
      });
      return this.is_ready = true;
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
      this.fpsLabel = new createjs.Text("-- fps", "bold 18px Arial", "#000");
      this.stage.addChild(this.fpsLabel);
      this.fpsLabel.x = 10;
      this.fpsLabel.y = 20;
      this.temp_arrow = this.new_arrow(0, 0, null);
      this.stage.addChild(this.temp_arrow);
      this.stage.update();
      createjs.Ticker.addListener(this);
      return createjs.Ticker.setFPS(50);
    };

    HexController.prototype.tick = function(time_passed) {
      if (this.update) {
        if (this.point_start && this.point_end) {
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

  retrieveBoardURL = "/game/board/";

  retrieveProgressURL = "/game/progress/";

  moveURL = "/game/move/";

  progressInterval = 1000;

  this.initBoard = function() {
    var board_id, me;
    me = $(this);
    board_id = me.attr("id");
    hexEnv.ajax(retrieveBoardURL, 2000, {
      board_id: board_id
    }, function(json) {
      var user_id;
      user_id = $("#user_id").val();
      hexEnv.initBoard(user_id, json.board_id, json[json.board_id], json.board_users, movethem);
      showBoardProgress(json.board_id);
    });
  };

  /*
    Shows game progress on the board.
    Moves, counts and colors
  */


  this.showBoardProgress = function(board_id) {
    hexEnv.ajax(retrieveProgressURL, 1000, {
      board_id: board_id
    }, function(json) {
      hexEnv.drawBoard(json.moves, json[json.board_id], json.board_users);
    });
    setTimeout("showBoardProgress(\"" + board_id + "\")", progressInterval);
  };

  movethem = function(from, to, board_id) {
    var params;
    params = {
      fx: from.x,
      fy: from.y,
      tx: to.x,
      ty: to.y,
      user_id: $("#user_id").val(),
      board_id: board_id
    };
    hexEnv.ajax(moveURL, 3000, params, function() {});
  };

}).call(this);
