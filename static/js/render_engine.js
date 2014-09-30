// Generated by CoffeeScript 1.4.0
(function() {
  var Cache, Cell, Graphics, RenderEngine;

  if (typeof d3 === "undefined" || d3 === null) {
    console.log("d3.js is not included. Consult with d3js.org");
    return;
  }

  if (typeof Backbone === "undefined" || Backbone === null) {
    console.log("backbone.js is not included. Consult with backbonejs.org");
    return;
  }

  Cache = {
    get: function(key, default_value) {
      if (key in this) {
        return this[key];
      } else {
        return default_value;
      }
    },
    set: function(key, value) {
      return this[key] = value;
    },
    call: function(key, func, context) {
      if (!(key in this)) {
        this[key] = func.apply(context, Array.prototype.slice.call(arguments, 3));
      }
      return this[key];
    }
  };

  Graphics = {
    board_offset: {
      x: 30,
      y: 30
    },
    animate: false,
    touch_detected: false,
    mouse_detected: false,
    rollback_queue: [],
    rollbackActions: function() {
      var args, context, func, item, _results;
      _results = [];
      while (item = this.rollback_queue.shift()) {
        func = item[0], context = item[1], args = item[2];
        if (args) {
          _results.push(func.apply(context, args));
        } else {
          _results.push(func.call(context));
        }
      }
      return _results;
    },
    createSVG: function(container_selector, width, height) {
      var self, svg;
      svg = d3.select(container_selector).append('svg').attr('width', width).attr('height', height);
      svg.on('touchstart', function() {
        svg.on('mousemove', null);
        svg.on('touchstart', null);
        return Graphics.touch_detected = true;
      }).on('mousemove', function() {
        svg.on('mousemove', null);
        svg.on('touchstart', null);
        return Graphics.mouse_detected = true;
      }).on('contextmenu', function() {
        return d3.event.preventDefault();
      });
      self = this;
      window.addEventListener('blur', function() {
        return self.rollbackActions.call(self);
      });
      window.addEventListener('mouseup', function() {
        return self.rollbackActions.call(self);
      });
      window.addEventListener('touchmove', function(e) {
        return e.preventDefault();
      });
      svg.append('g').attr('id', 'layer1');
      svg.append('g').attr('id', 'layer2');
      return svg;
    },
    Cell: Backbone.Model.extend({
      initialize: function() {
        this.initCoord();
        this.initContainer();
        this.initCircle();
        this.initArc();
        this.initHexagon();
        this.initArrow();
        this.initTmpArrow();
        this.on('change:power', this.changedPower, this);
        this.on('change:color', this.changedColor, this);
        return this.on('change:direction', this.changedDirection, this);
      },
      initCoord: function() {
        var coord, offset_x, offset_y, shift_x, sin_60;
        coord = this.get('coord');
        sin_60 = Math.sin(Math.PI / 3);
        offset_x = 2 * 30 * sin_60;
        offset_y = 2 * 30 * sin_60 * sin_60;
        shift_x = coord.y % 2 ? 0 : offset_x / 2;
        coord.x = coord.x * offset_x + Graphics.board_offset.x + shift_x;
        coord.y = coord.y * offset_y + Graphics.board_offset.y;
        return this.set('coord', coord);
      },
      initContainer: function() {
        var container, coord;
        container = this.get('svg').select('#layer1').append('g');
        coord = this.get('coord');
        container.attr('transform', "translate(" + coord.x + ", " + coord.y + ")");
        return this.set('container', container);
      },
      initCircle: function() {
        var angle, circle, color, container, radius, _ref;
        _ref = this._getRadiusAndAngle(), radius = _ref[0], angle = _ref[1];
        container = this.get('container');
        color = this.get('color');
        circle = container.append('circle').attr('r', radius).attr('fill', color);
        return this.set('circle', circle);
      },
      initArc: function() {
        var angle, arc, color, container, d, radius, _ref;
        _ref = this._getRadiusAndAngle(), radius = _ref[0], angle = _ref[1];
        container = this.get('container');
        color = this.get('color');
        d = d3.svg.arc().startAngle(0).innerRadius(radius).outerRadius(radius + 3).endAngle(angle);
        arc = container.append('path').attr('opacity', .5).attr('fill', color).attr('stroke', color).attr('stroke-width', 2).attr('stroke-linejoin', 'round').attr('d', d);
        return this.set('arc', arc);
      },
      initHexagon: function() {
        var angle, color, container, currX, currY, hexagon, i, points, self, _i;
        container = this.get('container');
        color = this.get('color');
        points = "";
        angle = Math.PI / 3;
        for (i = _i = 0; _i < 6; i = ++_i) {
          currX = Math.cos(i * angle + angle / 2) * 18;
          currY = Math.sin(i * angle + angle / 2) * 18;
          points += (i && "," || "") + currX + "," + currY;
        }
        hexagon = container.append("svg:polygon").attr('fill', color).attr('stroke', color).attr('stroke-width', 18).attr('opacity', .5).attr('points', points).style('stroke-linejoin', 'round');
        this.set('hexagon', hexagon);
        self = this;
        hexagon.on('mousedown', function() {
          return self.mouseDown.call(self);
        });
        hexagon.on('mouseup', function() {
          return self.mouseUp.call(self);
        });
        hexagon.on('mouseover', function() {
          return self.mouseOver.call(self);
        });
        hexagon.on('mouseout', function() {
          return self.mouseOut.call(self);
        });
        hexagon.on('touchstart', function() {
          return self.touchStart.call(self);
        });
        hexagon.on('touchmove', function() {
          return self.touchMove.call(self);
        });
        return hexagon.on('touchend', function() {
          return self.touchEnd.call(self);
        });
      },
      initArrow: function() {
        var arrow, color, container;
        container = this.get('svg').select('#layer2').append('g');
        color = this.get('color');
        arrow = container.append("svg:polygon").attr('stroke', color).attr('stroke-width', 5).attr("points", "0,0 10,10 0,5 -10,10 0,0").attr('stroke-linejoin', 'round').attr('visibility', 'hidden');
        this.set('arrow', arrow);
        if (this.get('direction')) {
          return this.changedDirection();
        }
      },
      initTmpArrow: function() {
        var arrow, svg;
        if (this.constructor.tmp_arrow) {
          return;
        }
        svg = this.get('svg');
        arrow = svg.append("svg:polygon").attr('stroke', '#ffff00').attr('stroke-width', 5).attr("points", "0,0 10,10 0,5 -10,10 0,0").attr('stroke-linejoin', 'round').attr('visibility', 'hidden');
        return this.constructor.tmp_arrow = arrow;
      },
      _powerToRadiusAndAngle: function(power) {
        var angle, max_radius, p, perimeter, radius, _i;
        angle = 0;
        p = power;
        max_radius = 21;
        for (radius = _i = 3; _i <= max_radius; radius = _i += 3) {
          perimeter = radius * 2 * Math.PI;
          if (p > perimeter) {
            if (radius >= max_radius) {
              break;
            }
            p -= perimeter;
          } else {
            angle = 2 * Math.PI * p / perimeter;
            break;
          }
        }
        return [radius, angle];
      },
      _getRadiusAndAngle: function() {
        var angle, fn, power;
        power = this.get('power');
        fn = this._powerToRadiusAndAngle;
        return angle = Cache.call("angle_for_" + power, fn, this, power);
      },
      changedPower: function() {
        var angle, d, radius, _ref;
        _ref = this._getRadiusAndAngle(), radius = _ref[0], angle = _ref[1];
        d = d3.svg.arc().startAngle(0).innerRadius(radius).outerRadius(radius + 3).endAngle(angle);
        this.get('arc').attr('d', d);
        return this.get('circle').attr('r', radius);
      },
      changedColor: function() {
        var color, container, t;
        color = this.get('color');
        this.get('circle').attr('fill', color);
        this.get('arc').attr('stroke', color).attr('fill', color);
        this.get('hexagon').attr('stroke', color).attr('fill', color);
        this.get('arrow').attr('stroke', color);
        if (!Graphics.animate) {
          return;
        }
        container = this.get('container');
        t = container.attr('transform');
        return container.attr('transform', t + ' scale(0.5, 0.5)').transition().attr('transform', t);
      },
      _transformArrow: function(arrow, d, offset) {
        var coord_x, coord_y, direction, t;
        d = parseInt(d);
        direction = d === 1 && 6 || d - 1;
        arrow.style('visibility', direction > 0 && 'visible' || 'hidden');
        if (!(direction > 0)) {
          return;
        }
        t = d3.transform();
        t.rotate = direction * 60 - 30;
        coord_x = Math.cos((direction - 2) * Math.PI / 3) * 30;
        coord_y = Math.sin((direction - 2) * Math.PI / 3) * 30;
        if (offset) {
          t.translate = [coord_x + offset.x, coord_y + offset.y];
        } else {
          t.translate = [coord_x, coord_y];
        }
        return arrow.attr('transform', t.toString());
      },
      changedDirection: function() {
        return this._transformArrow(this.get('arrow'), this.get('direction'), this.get('coord'));
      },
      tmpArrowTo: function(d) {
        if (!this.constructor.tmp_arrow) {
          return;
        }
        return this._transformArrow(this.constructor.tmp_arrow, d, this.get('coord'));
      },
      mouseDown: function() {
        if (Graphics.touch_detected) {
          return;
        }
        Graphics.rollbackActions();
        return this.get('parent').dragstart.call(this.get('parent'));
      },
      mouseUp: function() {
        if (Graphics.touch_detected) {
          return;
        }
        this.get('parent').dragstop.call(this.get('parent'));
        return Graphics.rollbackActions();
      },
      mouseOver: function() {
        if (Graphics.touch_detected) {
          return;
        }
        return this.get('parent').dragover.call(this.get('parent'));
      },
      mouseOut: function() {
        if (Graphics.touch_detected) {
          return;
        }
        this.tmpArrowTo(0);
        return this.get('parent').dragout.call(this.get('parent'));
      },
      touchStart: function() {
        if (Graphics.mouse_detected) {
          return;
        }
        Graphics.rollbackActions();
        return this.get('parent').dragstart();
      },
      touchMove: function() {
        var el, x, y, _i, _len, _ref, _ref1, _results;
        if (Graphics.mouse_detected) {
          return;
        }
        _ref = d3.mouse(this.get('svg')[0][0]), x = _ref[0], y = _ref[1];
        if (this.isPointInside(x, y)) {
          if (this.get('_is_hovered')) {
            return;
          }
          this.set('_is_hovered', true);
          return this.get('parent').dragover();
        } else {
          if (this.get('_is_hovered')) {
            this.set('_is_hovered', false);
            this.get('parent').dragout();
          }
          _ref1 = this.get('parent').getNeighbourElements();
          _results = [];
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            el = _ref1[_i];
            if (el.isPointInside(x, y)) {
              if (el.get('_is_hovered')) {
                continue;
              }
              el.set('_is_hovered', true);
              _results.push(el.get('parent').dragover());
            } else {
              if (!el.get('_is_hovered')) {
                continue;
              }
              el.set('_is_hovered', false);
              _results.push(el.get('parent').dragout());
            }
          }
          return _results;
        }
      },
      touchEnd: function() {
        var cur_el, el, x, y, _i, _len, _ref, _ref1;
        if (Graphics.mouse_detected) {
          return;
        }
        _ref = d3.mouse(this.get('svg')[0][0]), x = _ref[0], y = _ref[1];
        cur_el = null;
        if (this.isPointInside(x, y)) {
          cur_el = this;
        } else {
          _ref1 = this.get('parent').getNeighbourElements();
          for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
            el = _ref1[_i];
            if (el.isPointInside(x, y)) {
              cur_el = el;
            }
          }
        }
        if (cur_el) {
          if (cur_el.get('_is_hovered')) {
            cur_el.get('parent').dragout();
          }
          cur_el.get('parent').dragstop();
        }
        this.tmpArrowTo(0);
        return Graphics.rollbackActions();
      },
      isPointInside: function(x, y) {
        var coord, m, q2x, q2y, _hori, _vert;
        coord = this.get('coord');
        _vert = 27 / 2;
        _hori = 27 * Math.sqrt(3) / 2;
        q2x = Math.abs(x - coord.x);
        q2y = Math.abs(y - coord.y);
        if (q2x > _hori || q2y > _vert * 2) {
          return false;
        }
        m = 2 * _vert * _hori - _vert * q2x - _hori * q2y;
        return m >= 0;
      },
      animateHoverIn: function() {
        if (!Graphics.animate) {
          this.get('hexagon').attr('stroke-width', 24);
          return;
        }
        return this.get('hexagon').transition().attr('stroke-width', 24).ease('easeInOutCirc');
      },
      animateHoverOut: function() {
        if (!Graphics.animate) {
          this.get('hexagon').attr('stroke-width', 18);
          return;
        }
        return this.get('hexagon').transition().attr('stroke-width', 18).ease('easeInOutCirc');
      }
    })
  };

  Cell = Backbone.Model.extend({
    defaults: {
      neighbours: [],
      power: 50,
      color: "#cccccc",
      direction: 0
    },
    initialize: function() {
      var el;
      el = new Graphics.Cell({
        svg: this.get('svg'),
        color: this.get('color'),
        coord: _.clone(this.get('coord')),
        power: this.get('power'),
        direction: this.get('direction'),
        parent: this
      });
      this.set('el', el);
      this.on('change:power', this.powerChanged, this);
      this.on('change:color', this.colorChanged, this);
      return this.on('change:direction', this.directionChanged, this);
    },
    dragstart: function() {
      var cell, direction, _ref;
      if (!this.get('enabled')) {
        return;
      }
      _ref = this.get('neighbours');
      for (direction in _ref) {
        cell = _ref[direction];
        cell.set('drag_src', [direction, this]);
      }
      return Graphics.rollback_queue.push([
        function() {
          var _ref1, _results;
          _ref1 = this.get('neighbours');
          _results = [];
          for (direction in _ref1) {
            cell = _ref1[direction];
            _results.push(cell.set('drag_src', null));
          }
          return _results;
        }, this
      ]);
    },
    dragover: function() {
      var direction, drag_src, drag_src_info;
      drag_src_info = this.get('drag_src');
      if (!(this.get('enabled') || drag_src_info)) {
        return;
      }
      this.get('el').animateHoverIn();
      if (drag_src_info) {
        direction = drag_src_info[0], drag_src = drag_src_info[1];
        return drag_src.get('el').tmpArrowTo(direction);
      }
    },
    dragout: function() {
      var drag_src_info;
      drag_src_info = this.get('drag_src');
      if (!(this.get('enabled') || drag_src_info)) {
        return;
      }
      return this.get('el').animateHoverOut();
    },
    dragstop: function() {
      var args, dest_coord, direction, drag_src, drag_src_info, src_coord;
      drag_src_info = this.get('drag_src');
      if (drag_src_info) {
        this.get('el').animateHoverOut();
        direction = drag_src_info[0], drag_src = drag_src_info[1];
        src_coord = drag_src.get('coord');
        dest_coord = this.get('coord');
        args = [src_coord.x, src_coord.y, dest_coord.x, dest_coord.y];
        return this.get('renderengine').move.apply(this.get('renderengine'), args);
      }
    },
    getNeighbourElements: function() {
      var cell, d, _ref, _results;
      _ref = this.get('neighbours');
      _results = [];
      for (d in _ref) {
        cell = _ref[d];
        _results.push(cell.get('el'));
      }
      return _results;
    },
    colorChanged: function() {
      return this.get('el').set('color', this.get('color'));
    },
    powerChanged: function() {
      return this.get('el').set('power', this.get('power'));
    },
    directionChanged: function() {
      return this.get('el').set('direction', this.get('direction'));
    }
  });

  RenderEngine = (function() {

    RenderEngine.prototype.board = [];

    RenderEngine.prototype.svg = null;

    RenderEngine.prototype.user_id = null;

    RenderEngine.prototype.colors = {
      red: "#F72700",
      blue: "#447786",
      gray: "#C8C8C8"
    };

    function RenderEngine(container_id, width, height, user_id) {
      this.svg = Graphics.createSVG(container_id, width, height);
      this.user_id = user_id;
    }

    RenderEngine.prototype.updateBoard = function(board_users, board_powers, board_moves) {
      var color, d, direction, directions, fx, fy, has_cell_at, neighbours, pos, power, shift, tx, ty, user_id, x, y, _dummy_color, _i, _len, _ref, _ref1, _ref2;
      directions = {};
      for (y in board_users) {
        if (!(y in this.board)) {
          this.board[y] = [];
        }
        for (x in board_users[y]) {
          if (typeof board_users[y][x] === "object") {
            _ref = board_users[y][x], user_id = _ref[0], _dummy_color = _ref[1];
          } else {
            user_id = board_users[y][x];
          }
          power = board_powers[y][x];
          color = this._getColor(user_id);
          if (!(x in this.board[y])) {
            this.board[y][x] = this._newCellAt(x, y, color);
          }
          this.board[y][x].set('color', color);
          this.board[y][x].set('power', power);
          this.board[y][x].set('enabled', user_id === this.user_id);
          d = this.board[y][x].get('direction');
          if (d) {
            directions["" + y + "_" + x] = d;
          }
        }
      }
      for (_i = 0, _len = board_moves.length; _i < _len; _i++) {
        _ref1 = board_moves[_i], fx = _ref1[0], fy = _ref1[1], tx = _ref1[2], ty = _ref1[3];
        direction = this._getDirection(fx, fy, tx, ty);
        if (direction) {
          this.board[fy][fx].set('direction', direction);
          delete directions["" + fy + "_" + fx];
        }
      }
      for (pos in directions) {
        _ref2 = pos.split('_'), y = _ref2[0], x = _ref2[1];
        this.board[y][x].set('direction', 0);
      }
      has_cell_at = function(y, x) {
        if (y in board_users) {
          return x in board_users[y];
        }
        return false;
      };
      for (y in board_users) {
        for (x in board_users[y]) {
          y = parseInt(y);
          x = parseInt(x);
          shift = y % 2 ? 0 : 1;
          neighbours = [];
          if (has_cell_at(y - 1, x - 1 + shift)) {
            neighbours[1] = this.board[y - 1][x - 1 + shift];
          }
          if (has_cell_at(y - 1, x + shift)) {
            neighbours[2] = this.board[y - 1][x + shift];
          }
          if (has_cell_at(y, x + 1)) {
            neighbours[3] = this.board[y][x + 1];
          }
          if (has_cell_at(y + 1, x + shift)) {
            neighbours[4] = this.board[y + 1][x + shift];
          }
          if (has_cell_at(y + 1, x - 1 + shift)) {
            neighbours[5] = this.board[y + 1][x - 1 + shift];
          }
          if (has_cell_at(y, x - 1)) {
            neighbours[6] = this.board[y][x - 1];
          }
          this.board[y][x].set('neighbours', neighbours);
        }
      }
    };

    RenderEngine.prototype._getDirection = function(fx, fy, tx, ty) {
      var shift;
      shift = fy % 2 ? 0 : 1;
      if (ty === fy - 1 && tx === fx - 1 + shift) {
        return 1;
      }
      if (ty === fy - 1 && tx === fx + shift) {
        return 2;
      }
      if (ty === fy && tx === fx + 1) {
        return 3;
      }
      if (ty === fy + 1 && tx === fx + shift) {
        return 4;
      }
      if (ty === fy + 1 && tx === fx - 1 + shift) {
        return 5;
      }
      if (ty === fy && tx === fx - 1) {
        return 6;
      }
      return 0;
    };

    RenderEngine.prototype._newCellAt = function(x, y, color) {
      return new Cell({
        svg: this.svg,
        color: color,
        coord: {
          x: x,
          y: y
        },
        renderengine: this
      });
    };

    RenderEngine.prototype._getColor = function(user_id) {
      var i, num_users;
      if (!('_colors_assigned' in this)) {
        this._colors_assigned = {};
        this._colors_left = [this.colors.blue, this.colors.red];
      }
      if (user_id === 0) {
        return this.colors.gray;
      }
      if (user_id in this._colors_assigned) {
        return this._colors_assigned[user_id];
      }
      if (this._colors_left.length) {
        return this._colors_assigned[user_id] = this._colors_left.shift();
      }
      num_users = ((function() {
        var _results;
        _results = [];
        for (i in this._colors_assigned) {
          _results.push(i);
        }
        return _results;
      }).call(this)).length + 1;
      throw new Error("not enough colors for " + num_users + " users");
    };

    RenderEngine.prototype.move = function(fx, fy, tx, ty) {
      return console.log(fx, fy, tx, ty, this);
    };

    return RenderEngine;

  })();

  window.Engine = RenderEngine;

}).call(this);
