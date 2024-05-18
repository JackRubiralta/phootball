from __future__ import annotations
import math

class vec:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        
    def __add__(self, other: vec) -> vec:
        return vec(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: vec) -> vec:
        return vec(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: vec | float | int) -> vec:
        if isinstance(other, vec):
            return vec(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return vec(self.x * other, self.y * other)
        else:
            raise ValueError(f"Multiplication with type {type(other)} not supported")

    def __rmul__(self, other):
        """Called if 4 * self for instance"""
        return self.__mul__(other)

    def __truediv__(self, other: vec) -> vec:
        if isinstance(other, vec):
            return vec(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return vec(self.x / other, self.y / other)
        else:
            raise ValueError(f"Division with type {type(other)} not supported")
    
    def __str__(self) -> str:
        return f"<x: {self.x}, y: {self.y}>"

    def __iter__(self):
        yield self.x
        yield self.y

    @staticmethod
    def dist(vec1: vec, vec2: vec) -> float:
        return math.sqrt((vec1.x - vec2.x)**2.0 + (vec1.y - vec2.y)**2.0)

    @staticmethod
    def norm(vec: vec) -> float:
        return math.sqrt(vec.x**2 + vec.y**2)

    @staticmethod
    def dot(vec1: vec, vec2: vec) -> float:
        return vec1.x * vec2.x + vec1.y * vec2.y
    
    def rotate(self, radians: float | int, around: vec) -> vec:
        new_cx = (self.x - around.x) * math.cos(radians) - (self.y - around.y) * math.sin(radians)
        new_cy = (self.x - around.x) * math.sin(radians) + (self.y - around.y) * math.cos(radians)
        
        self.x = new_cx + around.x
        self.y = new_cy + around.y
        return self